# Contributing Guidelines

Thank you for your interest in contributing to DocuChatAI! 🎉
Contributions of all kinds --- bug fixes, features, documentation, and improvements --- are welcome.

Please take a moment to read these guidelines before getting started.

------------------------------------------------------------------------

## Prerequisites

Before contributing, ensure you have:

-   Python 3.9+
-   Git
-   AWS Account (with Kendra Index access)
-   OpenAI API Key
-   A basic understanding of FastAPI and Python

------------------------------------------------------------------------

## How to Contribute

### 1. Fork the Repository

Create a fork of this repository to your own GitHub account.

### 2. Clone Your Fork

``` bash
git clone https://github.com/your-username/DocuChatAI.git
cd DocuChatAI
```

### 3. Create a Feature Branch

``` bash
git checkout -b feature/short-descriptive-name
```

Examples:
- `feature/add-new-llm-provider`
- `fix/kendra-query-parsing`
- `docs/update-api-examples`

------------------------------------------------------------------------

### 4. Make Your Changes

-   Keep changes focused and minimal.
-   Follow existing project structure and patterns.
-   Ensure you update `.env.example` if you add new configuration options.
-   Avoid mixing unrelated changes in one commit.

------------------------------------------------------------------------

### 5. Build and Test Locally

Before submitting a PR, make sure the project runs and tests pass:

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run tests**:
    ```bash
    pytest tests/
    ```

> Pull requests that break tests or fail to follow the project structure may be rejected.

------------------------------------------------------------------------

### 6. Commit Your Changes

Use clear and meaningful commit messages:

- `feat: add support for local LLMs via Ollama`
- `fix: resolve race condition in CSV logging`
- `docs: improve Kendra setup instructions`

Avoid vague messages like `fix`, `changes`, or `update stuff`.

------------------------------------------------------------------------

### 7. Submit a Pull Request

Push your branch and open a Pull Request against the `main` branch using the provided [Pull Request Template](.github/PULL_REQUEST_TEMPLATE/pull_request_template.md).

------------------------------------------------------------------------

## Coding Guidelines

Please follow these rules to keep the codebase clean and consistent:

-   Follow **PEP 8** coding conventions.
-   Use meaningful names for functions, classes, and variables.
-   Maintain the **Singleton** pattern for core services as established in `src/services/`.
-   Log significant events using the `csv_logger` in `src/utils/logger.py`.
-   Add or update tests for new features and bug fixes in the `tests/` directory.

------------------------------------------------------------------------

## Pull Request Guidelines

-   One logical change per Pull Request.
-   Reference the related issue (if applicable).
-   Clearly explain what was changed and why.
-   Ensure all environment variables are documented in `.env.example`.

------------------------------------------------------------------------

## Reporting Bugs

Please use the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md) and include:

-   Steps to reproduce.
-   Expected vs Actual behavior.
-   Relevant logs from the `logs/` directory.
-   Python and FastAPI versions.

------------------------------------------------------------------------

## Code of Conduct

By participating in this project, you agree to abide by the project's Code of Conduct.

------------------------------------------------------------------------

Thank you again for contributing and helping improve DocuChatAI! 🙌
