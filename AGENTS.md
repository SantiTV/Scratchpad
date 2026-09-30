# AGENTS.md — Obsidian Quick Notes Sync

A lightweight, ultra-fast Markdown scratchpad web application built to capture quick notes and selectively sync them to a local Obsidian vault and Google Drive.

## Stack and structure
- Technologies: Python (standard libraries or lightweight frameworks like Flask; **NO FastAPI**), HTML/JavaScript frontend.
- Structure:
  - `app.py`: Main backend server handling requests, file management, local sync, and Google Drive API integration.
  - `templates/` or `static/`: Frontend interface for typing markdown, listing captured notes, and providing checkboxes for selective sync.
  - `config.json` or `.env`: Configuration file for local vault path and Google Drive credentials.
  - `MEMORY.md`: Project memory tracking recent status, technical decisions, and lessons learned.

## Commands
- Run app locally: `python app.py`
- Run tests: `pytest` (if applicable)
- Lint code: `flake8` or `black .`

## Conventions
- Code Style: Clean, modular Python functions; minimal external dependencies.
- Naming: Snake_case for Python variables/functions, camelCase or standard HTML IDs for frontend elements.
- Language: English for code comments, documentation, and agent prompts.

## Domain rules / Known pitfalls
- FastAPI restriction: **Do NOT use FastAPI** for this project's architecture.
- File system permissions: Ensure the backend has correct read/write permissions for the local Obsidian vault directory path.
- Google Drive API: Handle token expiry and OAuth/Service Account credentials securely without exposing secrets.

## Workflow
- Plan before coding: Outline changes for backend sync logic or frontend UI updates before writing code.
- Change size: Keep commits/changes small, incremental, and atomic.
- Completion wrap-up: Briefly explain what was accomplished and verify sync status before finishing.

## Boundaries
- ✅ Always: Ensure files are written cleanly in valid Markdown format.
- ✅ Always: Update `MEMORY.md` upon completing every task.
- ⚠️ Ask before: Installing new Python packages/dependencies, creating new core files, or modifying data sync structures.
- 🚫 Never: Hardcode sensitive data, API keys, or tokens directly into the codebase.

## Verification
- How to verify: Run the local server, type a test markdown note, select it via the UI checkboxes, trigger both local sync and Google Drive sync, and verify the files appear correctly in the target folders.

## Memory
- At start: Read `MEMORY.md` to understand project state and past decisions.
- At task completion: Update `MEMORY.md` with current status, key decisions (with reasoning), and pitfalls to avoid.
- Keep it concise: Max ~50 lines; summarize or prune outdated info.
- Rule promotion: If something becomes a permanent rule, propose moving it to `AGENTS.md`.
- No sensitive data: Never store secrets, tokens, or personal data in memory.