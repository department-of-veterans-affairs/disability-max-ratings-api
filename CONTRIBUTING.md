# Contributing to Disability Max Ratings API

Thank you for your interest in contributing to the Disability Max Ratings API! Contributions help us ensure this project continues to serve its purpose effectively. Whether you're fixing bugs, proposing enhancements, or improving documentation, your help is greatly appreciated.

## Table of Contents

1. [Getting Started](#getting-started)
2. [How to Contribute](#how-to-contribute)
    - [Reporting Issues](#reporting-issues)
    - [Feature Requests](#feature-requests)
    - [Code Contributions](#code-contributions)
3. [Pull Request Guidelines](#pull-request-guidelines)
4. [Style Guides](#style-guides)
5. [Resources](#resources)

---

## Getting Started

For detailed setup instructions, please refer to the [README.md](README.md).

---

## How to Contribute

### Reporting Issues

If you encounter a bug or have a question, please [open an issue](https://github.com/department-of-veterans-affairs/disability-max-ratings-api/issues) with the following information:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Relevant logs or screenshots, if applicable
- Environment details (e.g., OS, Python version, etc)

### Feature Requests

We welcome suggestions for new features! When submitting a feature request, please include:

- A description of the feature and its purpose
- Why it’s useful and how it aligns with the project’s goals
- Any implementation ideas, if you have them

### Code Contributions

To contribute code:

- Fork the repository, clone it locally, and create a new branch for your changes
- Follow the setup instructions in the [README.md](README.md#getting-started)
- Make your changes, adhering to the [Style Guides](#style-guides)
- Please ensure all tests pass and add new tests for any new functionality
- Commit your changes with clear and descriptive messages
- Push your changes and open a pull request for review
- Please ensure all CI checks pass before requesting a review

---

## Pull Request Guidelines

- Ensure your PR description clearly explains:
    - The purpose of the change
    - Any related issues (link to the issue, if applicable)
    - How the changes were tested
- Follow the project’s [Style Guides](#style-guides)
- Include tests for new features or fixes
- Keep PRs small
  - Focus on a single issue or feature
  - Avoid bundling unrelated changes; however, small "Boy Scout Rule" improvements are welcome
- Be responsive to feedback during the review process

---

## Style Guides

### Python Style Guide

The project follows the [PEP 8](https://pep8.org/) style guide for Python code using the ['ruff'](https://docs.astral.sh/ruff/) formatter with ['mypy'](https://mypy.readthedocs.io/) for type checking. Additionally, it uses ['bandit'](https://bandit.readthedocs.io/) for security checks.

If the [`pre-commit`](https://pre-commit.com/) hooks are installed, they will automatically run `ruff`, `mypy`, and `bandit` checks before committing changes.

### Git Commit Messages

- Must use [Commit Guide](docs/commitizen.md) to push commits to this repository.
- Use the imperative mood (e.g., "Add feature X" instead of "Added feature X")
- Keep the first line under 50 characters
- Provide additional details in subsequent lines, if necessary

---

## Resources

- [Python.org Documentation](https://docs.python.org/3.12/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Bandit Documentation](https://bandit.readthedocs.io/)

---

Thank you for contributing to the Disability Max Ratings API! Your efforts make a difference.

---

## Contact

If you have any questions or need assistance with contributing, feel free to reach out by opening an issue in the [repository](https://github.com/department-of-veterans-affairs/disability-max-ratings-api/issues) or contacting the maintainers directly through the issue tracker.
