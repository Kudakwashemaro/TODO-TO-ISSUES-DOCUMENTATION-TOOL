# TODO → GitHub Issues Automation

### Title-Based Anchoring with Rich Metadata

Automated conversion of structured TODO comments into **fully managed GitHub Issues**, using a **title-based anchoring system** that supports cross-file references, prioritization, categorization, and assignment — *without requiring issue numbers in code*.

This project is designed for teams that want disciplined, scalable, and auditable technical debt tracking directly from their codebase.

---

## Why This Exists

Traditional TODO comments are:

* Invisible to project planning
* Hard to track across files
* Easy to forget and never resolve

This tool turns TODOs into **first-class project artifacts**:

* One issue per concern
* Multiple code locations linked automatically
* Rich metadata for planning and prioritization
* Zero manual bookkeeping

---

## Core Concept: Title-Based Anchoring

**TODOs are bundled by a shared `TITLE` string.**

* One **Canonical TODO** creates the GitHub Issue
* Multiple **Reference TODOs** link to the same issue by matching the title
* Metadata drives labels, assignment, and categorization
* You do *not* need to know the issue number beforehand

This enables multi-file, cross-cutting TODOs without fragmentation.

---

## TODO Formats

### Canonical TODO (Creates the Issue)

Use **once per concern**, ideally where the primary work will occur.

```python
# TODO(TITLE: Fix race condition in user update): Happens when two requests run concurrently
```

With metadata:

```python
# TODO(
#   TITLE: Fix race condition in user update,
#   PRIORITY: high,
#   TYPE: bug,
#   ASSIGNEE: johndoe
# ): Concurrent updates cause data corruption
```

**Syntax**

```
TODO(TITLE: <Unique Title>, [METADATA...]) : [Optional Description]
```

---

### Reference TODO (Links to the Issue)

Use anywhere else the same concern applies.

```python
# TODO(REF: Fix race condition in user update): Also check this write path
```

**Rules**

* The `REF` title **must match the canonical TITLE exactly**
* The reference context is added to the issue checklist

---

## Supported Metadata

Metadata is read **only from the Canonical TODO**.

| Tag        | Purpose                  |         |          |               |      |             |          |                |
| ---------- | ------------------------ | ------- | -------- | ------------- | ---- | ----------- | -------- | -------------- |
| `PRIORITY` | `critical                | high    | medium   | low`          |      |             |          |                |
| `TYPE`     | `bug                     | feature | refactor | documentation | test | performance | security | accessibility` |
| `EFFORT`   | `small                   | medium  | large    | xlarge`       |      |             |          |                |
| `EPIC`     | Groups related issues    |         |          |               |      |             |          |                |
| `ASSIGNEE` | Auto-assigns GitHub user |         |          |               |      |             |          |                |

---

## Automatic Labeling

### Priority

* `priority:critical`
* `priority:high`
* `priority:medium` (default)
* `priority:low`

### Type

* `type:bug`
* `type:feature`
* `type:refactor`
* `type:documentation`
* `type:test`
* `type:performance`
* `type:security`
* `type:accessibility`

### Effort

* `effort:small` (< 2h)
* `effort:medium` (2–8h)
* `effort:large` (1–3 days)
* `effort:xlarge` (> 3 days)

### Always Applied

* `todo`
* `tech-debt`

Epic metadata generates labels like:

```
epic:oauth-migration
```

---

## How to Use This Template

1.  **Click "Use this template"** to create a new repository from this one.
2.  **That's it!** The workflow is pre-configured to run on every push to `main`.

### Configuration

You can customize the behavior by editing `.github/todo-config.yml`.

```yaml
default_labels: ['todo', 'tech-debt']
include_extensions: ['.py', '.js', '.ts']
exclude_directories: ['node_modules', 'dist']
auto_close: true
duplicate_threshold: 0.85
```

### Manual Usage (Dry Run)

You can run the script locally to see what issues would be created without actually creating them:

```bash
# Install dependencies
pip install -r .github/scripts/requirements.txt

# Run in dry-run mode
python3 .github/scripts/todo_to_issues.py --dry-run
```

## Live Demo in this Repository

This repository includes example files to demonstrate the workflow in action:

1.  **[example.py](example.py)**: Contains "Canonical" TODOs that define the Issues.
    *   Defines a critical feature: `Implement Payment Gateway Integration`.
    *   Defines a security fix: `Fix XSS vulnerability`.
    *   Demonstrates metadata usage: `PRIORITY`, `TYPE`, `EPIC`, `ASSIGNEE`.
2.  **[example_utils.py](example_utils.py)**: Contains "Reference" TODOs.
    *   Links back to the Payment Gateway issue from a different file.
    *   Shows how multiple files can track progress on the same Issue.

**What happens when you push?**
The workflow will parse these files and create Issues like:

*   **Issue 1:** `TODO: Implement Payment Gateway Integration`
    *   **Labels:** `priority:critical`, `type:feature`, `epic:monetization`
    *   **Body:** Includes a checklist linking to `example.py:5`, `example.py:9`, and `example_utils.py:10`.

## Workflow Behavior

1.  **Scan**: Runs on push to `main` or manually.
2.  **Match**: Groups TODOs by `TITLE`.
3.  **Create**: Creates a GitHub Issue if none exists for the title.
4.  **Update**: Updates existing issues with new references.
5.  **Auto-Close**: (Optional) Closes issues if the TODO is removed from the code.

**Troubleshooting**

*   Check GitHub Actions logs.
*   Ensure `GITHUB_TOKEN` has `issues: write` permission (default in new repos).


---

## Roadmap

Planned enhancements:

* Auto-close issues when all TODOs are removed
* Parent/child issue relationships
* Slack / Discord notifications
* Weekly TODO digest
* Metrics dashboard (age, density, resolution time)
* Due dates (`DUE: YYYY-MM-DD`)
* Deeper GitHub Projects automation

---

## Author

**Kudakwashe Marongedza**
Backend Developer | Django & API Specialist | SaaS Builder

* Portfolio: [https://kudakwashem.is-a.dev](https://kudakwashem.is-a.dev)
* Focus: scalable backends, workflow automation, developer tooling

---

## Contributing & Collaboration

This project is **open to collaboration**.

If you are interested in:

* Improving the parser
* Adding CI enforcement
* Extending metadata support
* Building analytics or dashboards
* Hardening the workflow for large teams

Please:

1. Open an issue with ideas or proposals
2. Submit a pull request
3. Or start a discussion

Use the label:

```
workflow-enhancement
```

Contributions, critiques, and real-world feedback are welcome.


