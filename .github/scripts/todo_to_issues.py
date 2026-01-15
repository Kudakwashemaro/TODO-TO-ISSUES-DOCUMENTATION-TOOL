import os
import re
import yaml
import argparse
from pathlib import Path
from github import Github
from collections import defaultdict
import textwrap
from difflib import SequenceMatcher

def load_config():
    """Load configuration from .github/todo-config.yml or return defaults."""
    config = {
        'default_labels': ['todo', 'tech-debt'],
        'include_extensions': ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.go', '.rs', '.rb', '.php', '.sh', '.bash'],
        'exclude_directories': ['.git', '.venv', 'venv', 'node_modules', '__pycache__', '.pytest_cache', 'dist', 'build'],
        'exclude_extensions': ['.md', '.txt', '.rst', '.html', '.xml', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg'],
        'auto_close': True,
        'duplicate_threshold': 0.85
    }

    config_path = Path('.github/todo-config.yml')
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    config.update(user_config)
            print(f"Loaded configuration from {config_path}")
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
    else:
        print("No configuration file found. Using defaults.")
    
    return config

def similarity_ratio(s1, s2):
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

def find_duplicate(title, existing_titles, threshold=0.85):
    """Find potential duplicate based on similarity threshold"""
    for existing_title in existing_titles:
        if similarity_ratio(title, existing_title) >= threshold:
            return existing_title
    return None

def parse_metadata(metadata_str):
    """Parse metadata string into dict of key-value pairs"""
    metadata = {}
    if not metadata_str:
        return metadata
    
    pairs = [p.strip() for p in metadata_str.split(',')]
    for pair in pairs:
        if ':' in pair:
            key, value = pair.split(':', 1)
            metadata[key.strip().upper()] = value.strip()
    
    return metadata

def extract_labels_from_metadata(metadata, config):
    """Convert metadata to GitHub labels"""
    labels = config['default_labels'].copy()
    
    # Label mapping for metadata
    PRIORITY_LABELS = {
        'critical': 'priority:critical',
        'high': 'priority:high',
        'medium': 'priority:medium',
        'low': 'priority:low'
    }
    
    TYPE_LABELS = {
        'bug': 'type:bug',
        'feature': 'type:feature',
        'refactor': 'type:refactor',
        'documentation': 'type:documentation',
        'test': 'type:test',
        'performance': 'type:performance',
        'security': 'type:security',
        'accessibility': 'type:accessibility'
    }
    
    EFFORT_LABELS = {
        'small': 'effort:small',
        'medium': 'effort:medium',
        'large': 'effort:large',
        'xlarge': 'effort:xlarge'
    }

    if 'PRIORITY' in metadata:
        priority = metadata['PRIORITY'].lower()
        if priority in PRIORITY_LABELS:
            labels.append(PRIORITY_LABELS[priority])
    
    if 'TYPE' in metadata:
        type_val = metadata['TYPE'].lower()
        if type_val in TYPE_LABELS:
            labels.append(TYPE_LABELS[type_val])
    
    if 'EFFORT' in metadata:
        effort = metadata['EFFORT'].lower()
        if effort in EFFORT_LABELS:
            labels.append(EFFORT_LABELS[effort])
    
    if 'EPIC' in metadata:
        labels.append(f"epic:{metadata['EPIC'].lower().replace(' ', '-')}")
    
    return labels

def main():
    parser = argparse.ArgumentParser(description='Convert TODOs to GitHub Issues')
    parser.add_argument('--token', help='GitHub Token', required=False)
    parser.add_argument('--repo', help='Repository Name (owner/repo)', required=False)
    parser.add_argument('--sha', help='Commit SHA', required=False)
    parser.add_argument('--dry-run', action='store_true', help='Do not create issues, just print what would happen')
    args = parser.parse_args()

    # Get credentials from args or env vars
    token = args.token or os.environ.get('GITHUB_TOKEN')
    repo_name = args.repo or os.environ.get('REPO_NAME')
    commit_sha = args.sha or os.environ.get('COMMIT_SHA') or 'unknown-sha'

    if not args.dry_run and (not token or not repo_name):
        print("Error: GITHUB_TOKEN and REPO_NAME are required for non-dry-run mode")
        return

    config = load_config()

    # Initialize GitHub client if not dry run
    repo = None
    if not args.dry_run:
        g = Github(token)
        repo = g.get_repo(repo_name)

    print("=" * 80)
    print("SCANNING REPOSITORY FOR TODOs")
    print("=" * 80)

    # Regex patterns for TODOs with optional metadata
    canonical_pattern = re.compile(
        r'#\s*TODO\(TITLE:\s*([^,)]+)(?:,\s*([^)]*))?\)(?::\s*(.*))?',
        re.IGNORECASE
    )
    referenced_pattern = re.compile(
        r'#\s*TODO\(REF:\s*([^,)]+)(?:,\s*([^)]*))?\)(?::\s*(.*))?',
        re.IGNORECASE
    )

    canonical_todos = {}
    referenced_todos = defaultdict(list)

    exclude_dirs = set(config['exclude_directories'])
    exclude_extensions = set(config['exclude_extensions'])
    code_extensions = set(config['include_extensions'])
    
    for file_path in Path('.').rglob('*'):
        if any(ex in file_path.parts for ex in exclude_dirs):
            continue
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() in exclude_extensions:
            continue
        if file_path.suffix.lower() not in code_extensions:
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    canon_match = canonical_pattern.search(line)
                    if canon_match:
                        raw_title = canon_match.group(1).strip()
                        metadata_str = canon_match.group(2)
                        extra_desc = canon_match.group(3).strip() if canon_match.group(3) else ""
                        
                        metadata = parse_metadata(metadata_str)
                        
                        full_desc = raw_title
                        if extra_desc:
                            full_desc += f": {extra_desc}"

                        if raw_title not in canonical_todos:
                            canonical_todos[raw_title] = {
                                'file': str(file_path),
                                'line': line_num,
                                'title': raw_title,
                                'description': full_desc,
                                'text': line.strip(),
                                'metadata': metadata,
                                'labels': extract_labels_from_metadata(metadata, config)
                            }
                        continue

                    ref_match = referenced_pattern.search(line)
                    if ref_match:
                        raw_title = ref_match.group(1).strip()
                        metadata_str = ref_match.group(2)
                        extra_desc = ref_match.group(3).strip() if ref_match.group(3) else ""
                        
                        metadata = parse_metadata(metadata_str)
                        
                        referenced_todos[raw_title].append({
                            'file': str(file_path),
                            'line': line_num,
                            'description': extra_desc if extra_desc else "Reference",
                            'text': line.strip(),
                            'metadata': metadata
                        })
                        continue

        except (UnicodeDecodeError, PermissionError) as e:
            if args.dry_run:
                print(f"Warning: Could not read {file_path}: {e}")
            continue

    print(f"\nFound {len(canonical_todos)} canonical TODO titles")
    print(f"Found {sum(len(v) for v in referenced_todos.values())} referenced TODOs")

    if args.dry_run:
        print("\n[DRY RUN] Skipping Issue Check and Creation")
        print("\nWOULD CREATE ISSUES FOR:")
        for title in canonical_todos:
            print(f" - {title}")
        return

    # Get existing issues with 'todo' label
    print("\n" + "=" * 80)
    print("CHECKING EXISTING ISSUES")
    print("=" * 80)
    
    existing_issues_map = {}
    try:
        for issue in repo.get_issues(state='all', labels=['todo']):
            if issue.title.startswith("TODO: "):
                extracted_title = issue.title[6:].strip()
                existing_issues_map[extracted_title] = issue
        
        print(f"Found {len(existing_issues_map)} existing TODO issues")
    except Exception as e:
        print(f"Error fetching existing issues: {e}")

    # AUTO-CLOSE: Close issues for TODOs that no longer exist
    print("\n" + "=" * 80)
    print("AUTO-CLOSING REMOVED TODOs")
    print("=" * 80)

    closed_count = 0
    if config['auto_close']:
        current_todo_titles = set(canonical_todos.keys())
        
        for existing_title, issue in existing_issues_map.items():
            if issue.state == 'open' and existing_title not in current_todo_titles:
                try:
                    issue.edit(state='closed')
                    issue.create_comment(
                        f"🤖 Auto-closed: TODO comment was removed from codebase in commit {commit_sha[:7]}"
                    )
                    print(f"\nClosed issue #{issue.number}: '{existing_title}' (TODO removed from code)")
                    closed_count += 1
                except Exception as e:
                    print(f"\nError closing issue #{issue.number}: {e}")
    else:
        print("Auto-close is disabled in configuration")

    print(f"\nClosed {closed_count} issue(s)")

    # Create issues for NEW canonical TODOs
    print("\n" + "=" * 80)
    print("CREATING ISSUES FOR CANONICAL TODOs")
    print("=" * 80)

    created_count = 0
    duplicate_count = 0
    
    for title_key, todo in canonical_todos.items():
        if title_key in existing_issues_map:
            print(f"\nSkipping (already exists): {title_key[:60]}...")
            continue

        duplicate_title = find_duplicate(
            title_key, 
            existing_issues_map.keys(), 
            threshold=config['duplicate_threshold']
        )
        
        if duplicate_title:
            print(f"\nPotential duplicate detected:")
            print(f"  New: '{title_key}'")
            print(f"  Existing: '{duplicate_title}'")
            print(f"  Similarity: {similarity_ratio(title_key, duplicate_title):.2%}")
            
            try:
                existing_issue = existing_issues_map[duplicate_title]
                permalink = f"https://github.com/{repo_name}/blob/{commit_sha}/{todo['file']}#L{todo['line']}"
                existing_issue.create_comment(
                    f"🔍 Potential duplicate TODO found:\n\n"
                    f"**Title:** {title_key}\n"
                    f"**Location:** [`{todo['file']}:{todo['line']}`]({permalink})\n\n"
                    f"This may be a duplicate or related TODO. Please review."
                )
            except Exception as e:
                print(f"  Could not add comment to existing issue: {e}")
            
            duplicate_count += 1
            continue

        try:
            permalink = f"https://github.com/{repo_name}/blob/{commit_sha}/{todo['file']}#L{todo['line']}"

            metadata_section = ""
            if todo['metadata']:
                metadata_section = "\n### Metadata\n"
                for key, value in todo['metadata'].items():
                    metadata_section += f"- **{key}**: {value}\n"

            body_content = textwrap.dedent(f"""
                **TODO:** {todo['description']}

                **Location:** `{todo['file']}:{todo['line']}`  
                **Permalink:** {permalink}  
                **Commit:** {commit_sha[:7]}
                {metadata_section}
                ---

                ### Code Context
                ```
                {todo['text']}
                ```

                ---

                ### Related TODO References
                _No related references found yet. References will be added automatically when found._
            """).strip()

            issue = repo.create_issue(
                title=f"TODO: {title_key}",
                body=body_content,
                labels=todo['labels']
            )

            if 'ASSIGNEE' in todo['metadata']:
                try:
                    assignee = todo['metadata']['ASSIGNEE']
                    issue.add_to_assignees(assignee)
                    print(f"   Assigned to: {assignee}")
                except Exception as e:
                    print(f"   Could not assign to {assignee}: {e}")

            print(f"\nCreated issue #{issue.number}: {title_key}")
            print(f"   Labels: {', '.join(todo['labels'])}")
            created_count += 1
            existing_issues_map[title_key] = issue

        except Exception as e:
            print(f"\nError creating issue for '{title_key}': {e}")

    print(f"\nCreated {created_count} new issues")
    print(f"Skipped {duplicate_count} potential duplicates")

    # Update issues with referenced TODOs
    print("\n" + "=" * 80)
    print("UPDATING ISSUES WITH CROSS-REFERENCES")
    print("=" * 80)

    updated_count = 0
    all_titles_with_refs = set(referenced_todos.keys())
    
    for title_key in all_titles_with_refs:
        if title_key not in existing_issues_map:
            print(f"\nFound {len(referenced_todos[title_key])} reference(s) for '{title_key}' but no canonical TODO or existing issue. Skipping.")
            continue
        
        issue = existing_issues_map[title_key]
        refs = referenced_todos[title_key]

        try:
            existing_refs_in_body = set()
            if issue.body:
                for line in issue.body.split('\n'):
                    if line.strip().startswith('- [ ]') and '`' in line:
                        match = re.search(r'`([^`]+:\d+)`', line)
                        if match:
                            existing_refs_in_body.add(match.group(1))

            new_refs_lines = []
            for ref in refs:
                ref_key = f"{ref['file']}:{ref['line']}"
                if ref_key not in existing_refs_in_body:
                    permalink = f"https://github.com/{repo_name}/blob/{commit_sha}/{ref['file']}#L{ref['line']}"
                    new_refs_lines.append(f"- [ ] [`{ref_key}`]({permalink}) – {ref['description']}")

            if new_refs_lines:
                new_body = issue.body or ""
                header = "### Related TODO References"
                
                if header not in new_body:
                    new_body += f"\n\n{header}\n" + "\n".join(new_refs_lines)
                else:
                    lines = new_body.split('\n')
                    header_idx = None
                    for i, line in enumerate(lines):
                        if header in line:
                            header_idx = i
                            break
                    
                    if header_idx is not None:
                        section_end = len(lines)
                        for i in range(header_idx + 1, len(lines)):
                            if lines[i].startswith('###'):
                                section_end = i
                                break
                        
                        before = '\n'.join(lines[:header_idx + 1])
                        existing_refs = '\n'.join(lines[header_idx + 1:section_end])
                        after = '\n'.join(lines[section_end:]) if section_end < len(lines) else ""
                        
                        new_body = before + '\n' + existing_refs + '\n' + '\n'.join(new_refs_lines)
                        if after:
                            new_body += '\n' + after
                
                issue.edit(body=new_body)
                print(f"\nUpdated issue #{issue.number} ('{title_key}') with {len(new_refs_lines)} new reference(s)")
                updated_count += 1
            else:
                print(f"\nIssue #{issue.number} already has all references for '{title_key}'")

        except Exception as e:
            print(f"\nError updating issue #{issue.number}: {e}")

    print(f"\nUpdated {updated_count} issue(s) with cross-references")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Canonical TODOs found: {len(canonical_todos)}")
    print(f"Issues created: {created_count}")
    print(f"Issues updated: {updated_count}")
    print(f"Issues closed: {closed_count}")
    print(f"Duplicates skipped: {duplicate_count}")
    print("=" * 80)

if __name__ == "__main__":
    main()
