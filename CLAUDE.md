# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Communication Language
- Communicate in Japanese (日本語) when interacting with users in this repository
- Use appropriate Japanese technical terminology for GitHub Actions and development concepts

## Repository Overview

This is a GitHub Actions study repository that demonstrates various GitHub Actions workflows and automation patterns. The repository contains multiple workflow examples for learning and testing GitHub Actions functionality.

## Common Commands

### Testing
- `make test` - Run basic test command
- `make act-manual` - Manually trigger GitHub Actions workflow via API

### GitHub Actions Workflow Management
- Workflows are located in `.github/workflows/`
- Use `gh workflow run` to manually trigger workflows
- Use `gh workflow list` to view available workflows

## Architecture & Structure

### GitHub Actions Workflows
The repository contains several example workflows:

1. **Manual Workflow** (`manual.yml`) - Basic manually triggered workflow with input parameters
2. **Stale Issues/PRs** (`stale.yml`) - Automated stale issue management with scheduled runs
3. **After Workflow** (`after.yml`) - Demonstrates workflow chaining using `workflow_run` trigger
4. **Claude Code Review** (`claude-code-review.yml`) - Automated code review using Claude on PRs
5. **Claude PR Assistant** (`claude.yml`) - Issue and PR assistance using Claude with @claude mentions

### Key Features
- **Workflow Triggers**: Examples of various trigger types (manual, scheduled, PR events, comments)
- **Workflow Chaining**: `after.yml` shows how to chain workflows using `workflow_run`
- **Claude Integration**: Two workflows demonstrate Claude Code integration for automated assistance and code review
- **API Integration**: `Makefile` shows how to manually trigger workflows via GitHub API

### Security Considerations
- The repository uses `CLAUDE_CODE_OAUTH_TOKEN` secret for Claude integration
- Workflows have appropriate permission scopes defined
- Code review workflow includes filters for draft PRs and skip markers

## Workflow Development

When working with workflows:
- Test manually with `workflow_dispatch` before implementing automated triggers
- Use appropriate permissions for each job
- Consider using conditional execution with `if` statements
- Follow GitHub Actions best practices for security and performance