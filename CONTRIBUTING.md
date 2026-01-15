# Contributing to TODO-to-Issues

Thank you for your interest in contributing to the TODO-to-Issues Document Tool! We welcome contributions from the community to help make this template better for everyone.

## How to Contribute

1.  **Fork the repository** and create your branch from `main`.
2.  **Make your changes**.
3.  **Run Tests**: Ensure all unit tests pass before submitting.
4.  **Submit a Pull Request**.

## Local Development

To set up the project locally:

1.  **Clone the repo**:
    ```bash
    git clone https://github.com/yourusername/TODO-to-Issues-Doc-Tool.git
    cd TODO-to-Issues-Doc-Tool
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r .github/scripts/requirements.txt
    ```

3.  **Run Tests**:
    ```bash
    python3 -m unittest discover .github/tests
    ```

4.  **Dry Run the Script**:
    You can test the logic against the local files without needing API access:
    ```bash
    python3 .github/scripts/todo_to_issues.py --dry-run
    ```

## Coding Standards

*   **Python**: We follow PEP 8. Please ensure your code is formatted cleanly.
*   **Tests**: New features should include unit tests in `.github/tests/`.
*   **Documentation**: Update the README if you change any user-facing functionality or configuration options.

## Reporting Issues

If you find a bug or have a feature request, please [open an issue](https://github.com/Kudakwashemaro/TODO-to-Issues-Doc-Tool/issues).
