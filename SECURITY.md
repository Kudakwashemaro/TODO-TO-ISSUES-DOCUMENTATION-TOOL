# Security Policy

## Supported Versions

Since this is a template repository and a development tool, we generally only support the latest version on the `main` branch.

| Version | Supported          |
| ------- | ------------------ |
| `main`  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please **DO NOT** create a public issue.

Instead, please report it via privacy email(kudakwashemaro@gmail.com) or the GitHub "Report a vulnerability" tab if enabled.

1.  Describe the vulnerability.
2.  Provide steps to reproduce.
3.  We will review and respond as quickly as possible.

## Security Best Practices for Users

*   **Token Scope**: This tool requires a `GITHUB_TOKEN` with `issues: write` permission. By default, GitHub Actions provides a token with scope limited to the repository running the action.
*   **Secrets**: Never commit your PAT (Personal Access Token) directly to code. Always use GitHub Secrets.
