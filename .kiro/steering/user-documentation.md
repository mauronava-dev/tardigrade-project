# User Documentation Guidelines

## Overview

The `docs/user` directory contains project-relevant documentation provided by developers. These files are gitignored but serve as important context for understanding the project.

## Agent Behavior

When working on this project, the agent MUST:

1. Check if `docs/user` directory exists
2. Read all documents within `docs/user` to gather project context
3. Consider this documentation when making decisions about implementation, architecture, or business logic

## Directory Structure

```
docs/
└── user/           # Developer-provided documentation (gitignored)
    ├── *.md        # Markdown documents
    ├── *.txt       # Text files
    ├── *.pdf       # PDF documents (if readable)
    └── ...         # Any other relevant documentation
```

## Document Types

Developers may include:

- API specifications (OpenAPI, GraphQL schemas)
- Business requirements documents
- Architecture decision records (ADRs)
- Integration guides
- Third-party service documentation
- Meeting notes or design discussions
- Any other project-relevant context

## Usage

Before starting significant work on the project:

```
1. List contents of docs/user directory
2. Read relevant documents based on the task at hand
3. Use the information to inform implementation decisions
```

## Important Notes

- Files in `docs/user` are gitignored and not version controlled
- Each developer may have different documents in this folder
- Treat these documents as supplementary context, not as source of truth
- When in doubt, ask the developer for clarification
