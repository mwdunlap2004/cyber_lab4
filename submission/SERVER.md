# My MCP Server

## What it does

`my_server.py` exposes two MCP tools over stdio:

- `list_notes()` lists readable note files in `notes/`
- `read_note(name)` returns the contents of a requested note

The corresponding VS Code server registration lives in `.vscode/mcp.json`.

## VS Code setup

1. Open the `submission/` folder in VS Code or Code Server.
2. Install the MCP SDK in the Python environment VS Code will use: `python -m pip install mcp`
3. Open `.vscode/mcp.json`.
4. Start the `my-server` entry from the Run button or from `MCP: List Servers`.
5. In Copilot agent mode, call `read_note` with `welcome.txt` and capture the transcript or screenshot.

## Planted vulnerability

- Taxonomy: path traversal
- Realistic mistake: the server joins user input onto `notes/` and reads the result without normalizing or enforcing the directory boundary
- Root cause: `read_note` trusts `name` and directly evaluates `NOTES_DIR / name`
- Fix: `my_server_secure.py` resolves the candidate path and only serves `.txt` files whose resolved parent is exactly `notes/`

## MCP transcript

This transcript comes from the MCP client in `attack_my_server.py`, which talks to the server over stdio using the same protocol VS Code uses.

### Vulnerable server

```text
$ python attack_my_server.py
Processing request of type ListToolsRequest
Processing request of type CallToolRequest
Processing request of type CallToolRequest
tools: ['list_notes', 'read_note']

[benign] read_note('welcome.txt'):
Welcome to my MCP server! This note lives in notes/welcome.txt and is safe to read.

[attack] read_note('../secret.txt'):
TOP SECRET — this file lives OUTSIDE notes/.
flag{you_escaped_the_notes_sandbox}

✓ ATTACK SUCCEEDED — read a file outside notes/.
```

### Secure server

```text
$ python attack_my_server.py my_server_secure.py
Processing request of type ListToolsRequest
Processing request of type CallToolRequest
Processing request of type CallToolRequest
tools: ['list_notes', 'read_note']

[benign] read_note('welcome.txt'):
Welcome to my MCP server! This note lives in notes/welcome.txt and is safe to read.

[attack] read_note('../secret.txt'):
Error executing tool read_note: note must stay inside the notes directory

✗ attack did not land (or you're running the secure server).
```

## VS Code transcript capture

I could not capture a real VS Code screenshot or transcript from this terminal-only environment, so this last artifact still needs one manual editor run. Use VS Code or Code Server on Rivanna with `.vscode/mcp.json`, then capture one tool call for submission:

1. Open `assignment-build/`
2. Run the `my-server` entry from `.vscode/mcp.json`
3. In Copilot agent mode, call `read_note` with `welcome.txt`
4. Paste the resulting VS Code transcript or screenshot into this section before submission
