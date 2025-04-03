# Email MCP Manager

A simple email manager that uses Ollama and Model Context Protocol (MCP) to analyze emails and suggest which ones to delete.

## Setup

1. Install Ollama following instructions at [ollama.com](https://ollama.com)

2. Pull a model with good function calling capabilities:
   ```bash
   ollama pull qwen2.5:3b
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your email settings in the `.env` file:
   ```
   EMAIL_USER=your_email@example.com
   EMAIL_PASSWORD=your_password
   EMAIL_SERVER=imap.example.com
   EMAIL_PORT=993
   ```

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```

2. Talk to the AI about your emails. Some example prompts:

   - "Analyze my 10 most recent emails and suggest which ones I can delete"
   - "Fetch my recent promotional emails and tell me which ones are safe to delete"
   - "Get my emails from yesterday and help me clean up my inbox"

3. Type 'exit' to quit the application.

## How It Works

This application uses the Model Context Protocol (MCP) to connect Ollama with your email account:

- The `email_fetcher.py` module provides functions to access your email via IMAP
- The `mcp_email_server.py` implements an MCP server that exposes email operations as tools
- The `main.py` script connects Ollama to the MCP server using mcphost

## Effective Prompts

For best results, try prompts like:

```
Please review my recent emails. For each email, analyze:
1. Sender importance (personal, work, marketing, etc.)
2. Content relevance to my interests
3. Whether it contains important information I need to keep
4. Whether it's outdated or no longer relevant

Then suggest which emails I can safely delete and provide a brief explanation for each.
```

## Security Note

This application stores your email credentials in a local `.env` file. Make sure to keep this file secure and don't share it with others.
