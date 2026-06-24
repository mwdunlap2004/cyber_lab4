"""my_server_secure.py — hardened variant of the lab MCP server."""

from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server-secure")

BASE_DIR = Path(__file__).parent
NOTES_DIR = (BASE_DIR / "notes").resolve()


@mcp.tool()
def list_notes() -> str:
    """List the note files available to read."""
    return "\n".join(sorted(p.name for p in NOTES_DIR.glob("*.txt"))) or "(no notes)"


@mcp.tool()
def read_note(name: str) -> str:
    """Read a note by name from the notes/ directory and return its text."""
    candidate = (NOTES_DIR / name).resolve()

    if candidate.suffix != ".txt":
        raise ValueError("only .txt notes are readable")
    if candidate.parent != NOTES_DIR:
        raise ValueError("note must stay inside the notes directory")
    if not candidate.is_file():
        raise FileNotFoundError(f"note not found: {name}")

    return candidate.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
