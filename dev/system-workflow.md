# System Workflow

## Project Awareness & Context

- **Always read `dev/product-requirements.md` and `dev/development.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
- **Check `dev/tasks.md`** before starting a new task. If the task isn’t listed, add it with a brief description and today's date.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `dev/development.md`.

## Task Completion

- **Mark completed tasks in `dev/tasks.md`** immediately after finishing them.
- Add new dependencies installed during a task execution to the dependency list,

## Documentation & Explainability

- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.
- **Update `dev/product-requirements.md` and `/dev/development.md`** if tasks done, expand or modify any of them.

## AI Behavior Rules

- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `dev/tasks.md`.

## Code Structure & Modularity

- **Never create a file longer than 800 lines of code, except for single file applications.**
    - If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
- **Use clear, consistent imports**, prefer relative imports within packages.
