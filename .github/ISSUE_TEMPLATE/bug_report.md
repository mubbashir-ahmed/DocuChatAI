---
name: Bug Report
about: Report a bug in DocuChatAI to help us improve
title: "[BUG] "
labels: bug
assignees: ""
---

## Describe the Bug
<!-- A clear and concise description of what the bug is -->

## Environment & Configuration
- **FastAPI Version**: (e.g., 0.128.0)
- **Python Version**: (e.g., 3.11)
- **AWS Kendra Index Status**: [Set up / Incomplete]
- **OpenAI Model**: [gpt-3.5-turbo / gpt-4o / Other]

## Steps to Reproduce
1. Start the server with `uvicorn src.api:app --reload`
2. Send a POST request to `/chatbot` with query '...'
3. See error or unexpected response

## Expected Behavior
<!-- What you expected to happen -->

## Actual Behavior
<!-- What actually happened -->

## Relevant Logs
<!-- Please include snippets from your logs/ (CSV logger output) or console if applicable -->
```csv
timestamp,level,message,exception
...
```

## Additional Context
<!-- Any other context about the problem, like specific document types in Kendra or networking setup -->
