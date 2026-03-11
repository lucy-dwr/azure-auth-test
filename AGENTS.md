# AGENTS.md

## Purpose

This repository demonstrates best-practice authentication for Microsoft Graph API and connects to a SharePoint list, as described in `README.md`.

## Scope and Priority

- This file applies to the entire repository.
- Follow direct user instructions first, then this file.
- Keep changes minimal, focused, and consistent with existing project patterns.

## Repository Context

- Main script: `fetch_sharepoint_list.py`
- Setup script: `scripts/setup.sh`
- Core docs: `README.md`, `docs/entra-setup.md`

## Allowed by Default

- Edit code and documentation in this repository.
- Run local verification commands.
- Run `./scripts/setup.sh` when environment setup is needed.

## Requires Explicit User Approval

- Running `git push`.
- Deleting files.
- Running the script against real Microsoft Graph/SharePoint endpoints.
- Installing dependencies via commands other than `./scripts/setup.sh`.

If an action is potentially dangerous or high-impact and is not listed above, ask before proceeding.

## Setup and Run Commands

- Setup: `./scripts/setup.sh`
- Run script: `.venv/bin/python fetch_sharepoint_list.py`

## Verification Standard

When code changes are made:

1. Ensure syntax validity:
   - `.venv/bin/python -m py_compile fetch_sharepoint_list.py`
2. If behavior or usage changes, update docs for consistency:
   - `README.md`
   - `docs/entra-setup.md`

## Done Bar

A task is complete when:

- Changed Python code compiles.
- Documentation is updated when needed.
- No secrets or credentials are introduced into tracked files.

## Coding and Style

- Follow PEP 8.
- Prefer clear, readable code over clever shortcuts.
- Keep functions and changes small and focused.

## Secrets and Sensitive Data

- Treat credentials as sensitive, especially values in `.env` (`MS_CLIENT_ID`, `MS_TENANT_ID`, tokens, and similar secrets).
- Never commit credentials or token caches.
- If uncertain whether data is sensitive, ask the user before committing.

## Commit Guidance

Do not create commits by default. Only create a commit when the user explicitly requests one.

Write commits as small, self-contained units:

- Use a short, descriptive subject line.
- Explain why the change was needed, not only what changed.
- Summarize key modifications and any user-visible effects.
- Note verification performed (for example, compile check, docs sync).
