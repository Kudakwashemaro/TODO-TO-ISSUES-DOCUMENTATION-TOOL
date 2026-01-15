# TODO → GitHub Issues Automation

<p align="center">
  <img width="1020" height="556" alt="TODO-TO-ISSUES" src="https://github.com/user-attachments/assets/4056f73f-3462-4373-a411-9adb19b619d2" />
</p>

<p align="center">
  <a href="https://github.com/Kudakwashemaro/TODO-TO-ISSUES-DOCUMENTATION-TOOL/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Kudakwashemaro/TODO-TO-ISSUES-DOCUMENTATION-TOOL" alt="License"></a>
  <a href="https://github.com/Kudakwashemaro/TODO-TO-ISSUES-DOCUMENTATION-TOOL/stargazers"><img src="https://img.shields.io/github/stars/Kudakwashemaro/TODO-TO-ISSUES-DOCUMENTATION-TOOL" alt="Stars"></a>
  <a href="https://github.com/Kudakwashemaro/TODO-TO-ISSUES-DOCUMENTATION-TOOL/wiki"><img src="https://img.shields.io/badge/docs-wiki-blue" alt="Wiki"></a>
</p>

<p align="center">
  <strong>Title-Based Anchoring with Rich Metadata</strong><br>
  Automated conversion of structured TODO comments into <strong>fully managed GitHub Issues</strong>
</p>

---

## 📖 Table of Contents

- [Quick Start](#-quick-start)
- [Why This Exists](#-why-this-exists)
- [Core Concept](#-core-concept-title-based-anchoring)
- [TODO Formats](#-todo-formats)
- [Supported Metadata](#-supported-metadata)
- [Configuration](#-configuration)
- [Live Demo](#-live-demo)
- [Workflow Behavior](#-workflow-behavior)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Author](#-author)

---

## 🚀 Quick Start

### Option 1: Use This Template (Recommended)

1. Click **"Use this template"** → **"Create a new repository"**
2. **That's it!** The workflow runs automatically on every push to `main`

### Option 2: Add to Existing Repository

Copy these files to your repository:

```
.github/
├── scripts/
│   ├── todo_to_issues.py
│   └── requirements.txt
├── workflows/
│   └── todo-to-issues.yml
└── todo-config.yml
```

### Test Locally (Dry Run)

```bash
pip install -r .github/scripts/requirements.txt
python3 .github/scripts/todo_to_issues.py --dry-run
```

> 📚 **Full documentation available in the [Wiki](https://github.com/Kudakwashemaro/TODO-TO-ISSUES-DOCUMENTATION-TOOL/wiki)**

---

## 💡 Why This Exists

Traditional TODO comments are:

- ❌ Invisible to project planning
- ❌ Hard to track across files
- ❌ Easy to forget and never resolve

This tool turns TODOs into **first-class project artifacts**:

- ✅ One issue per concern
- ✅ Multiple code locations linked automatically
- ✅ Rich metadata for planning and prioritization
- ✅ Zero manual bookkeeping

---

## 🎯 Core Concept: Title-Based Anchoring

**TODOs are bundled by a shared `TITLE` string.**

| Concept | Description |
|---------|-------------|
| **Canonical TODO** | Creates the GitHub Issue (use once per concern) |
| **Reference TODO** | Links to the same issue by matching the title |
| **Metadata** | Drives labels, assignment, and categorization |

> You do *not* need to know the issue number beforehand. This enables multi-file, cross-cutting TODOs without fragmentation.

---

## 📝 TODO Formats

### Canonical TODO (Creates the Issue)

Use **once per concern**, ideally where the primary work will occur:

```python
# TODO(TITLE: Fix race condition in user update): Happens when two requests run concurrently
```

With metadata:

```python
# TODO(TITLE: Fix race condition in user update, PRIORITY: high, TYPE: bug, ASSIGNEE: johndoe): Concurrent updates cause data corruption
```

### Reference TODO (Links to the Issue)

Use anywhere else the same concern applies:

```python
# TODO(REF: Fix race condition in user update): Also check this write path
```

> ⚠️ The `REF` title **must match the canonical TITLE exactly**

---

## 🏷️ Supported Metadata

| Tag | Values | Purpose |
|-----|--------|---------|
| `PRIORITY` | `critical`, `high`, `medium`, `low` | Issue priority level |
| `TYPE` | `bug`, `feature`, `refactor`, `documentation`, `test`, `performance`, `security`, `accessibility` | Issue category |
| `EFFORT` | `small` (<2h), `medium` (2-8h), `large` (1-3d), `xlarge` (>3d) | Estimated effort |
| `EPIC` | Any string | Groups related issues (becomes `epic:your-epic` label) |
| `ASSIGNEE` | GitHub username | Auto-assigns the issue |

### Automatic Labels

All issues automatically receive `todo` and `tech-debt` labels, plus any metadata-derived labels like `priority:high`, `type:bug`, etc.

---

## ⚙️ Configuration

Customize behavior via `.github/todo-config.yml`:

```yaml
default_labels: ['todo', 'tech-debt']
include_extensions: ['.py', '.js', '.ts']
exclude_directories: ['node_modules', 'dist']
auto_close: true
duplicate_threshold: 0.85
```

> 📖 See [Configuration](https://github.com/Kudakwashemaro/TODO-TO-ISSUES-DOCUMENTATION-TOOL/wiki/Configuration) in the wiki for all options.

---

## 🎬 Live Demo

This repository includes example files:

| File | Purpose |
|------|---------|
| [example.py](example.py) | Canonical TODOs with metadata |
| [example_utils.py](example_utils.py) | Reference TODOs linking to the same issues |

**On push, the workflow creates issues like:**

- **TODO: Implement Payment Gateway Integration**
  - Labels: `priority:critical`, `type:feature`, `epic:monetization`
  - Body: Checklist with all file locations

---

## 🔄 Workflow Behavior

```
Code Push → Scan TODOs → Match by Title → Create/Update Issues
```

1. **Scan**: Runs on push to `main` or manually
2. **Match**: Groups TODOs by `TITLE`
3. **Create**: Creates a GitHub Issue if none exists
4. **Update**: Adds new references to existing issues
5. **Auto-Close**: Closes issues when TODOs are removed (if enabled)

---

## 🗺️ Roadmap

| Feature | Status |
|---------|--------|
| Title-based anchoring | ✅ Done |
| Rich metadata support | ✅ Done |
| Auto-close issues | ✅ Done |
| Duplicate detection | ✅ Done |
| Multi-line TODOs | 🔜 Planned |
| Due date support | 🔜 Planned |
| Slack/Discord notifications | 🔜 Planned |
| VSCode extension | 🔜 Planned |

> 📖 See the full [Roadmap](https://github.com/Kudakwashemaro/TODO-TO-ISSUES-DOCUMENTATION-TOOL/wiki/Roadmap) in the wiki.

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to contribute:**

- Improve the parser
- Add support for more comment styles
- Build analytics or dashboards
- Add CI enforcement
- Write documentation

Use the label `workflow-enhancement` for related issues.

---

## 👤 Author

**Kudakwashe Marongedza**  
Backend Developer | Django & API Specialist | SaaS Builder

- 🌐 Portfolio: [kudakwashem.is-a.dev](https://kudakwashem.is-a.dev)
- 💻 Focus: Scalable backends, workflow automation, developer tooling

---

<p align="center">
  <a href="https://github.com/Kudakwashemaro/TODO-TO-ISSUES-DOCUMENTATION-TOOL/wiki">📖 Wiki</a> •
  <a href="https://github.com/Kudakwashemaro/TODO-TO-ISSUES-DOCUMENTATION-TOOL/issues">🐛 Issues</a> •
  <a href="https://github.com/Kudakwashemaro/TODO-TO-ISSUES-DOCUMENTATION-TOOL/discussions">💬 Discussions</a>
</p>
