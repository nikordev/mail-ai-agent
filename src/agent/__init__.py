from os import getenv
from typing import cast

from fastmcp import FastMCP
from fastmcp.server.server import Transport

from src.agent.tools.find_emails import FindMailsController
from src.agent.tools.load_emails import LoadMailsController


def make_load_emails():
    return LoadMailsController(
        ollama_url=getenv("OLLAMA_URL", "http://ollama:11434"),
        pop3_host=getenv("POP3_HOST", "mail-ai-agent-mailpit-1"),
        pop3_port=int(getenv("POP3_PORT", 1110)),
        pop3_user=getenv("POP3_USER", "user"),
        pop3_pass=getenv("POP3_PASS", "password"),
        pop3_ssl=int(getenv("POP3_SSL", 0)),
        pop3_debug=int(getenv("POP3_DEBUG", 0))
    )

def make_find_emails():
    return FindMailsController(
        ollama_url=getenv("OLLAMA_URL", "http://ollama:11434")
    )

def make_mcp() -> FastMCP:
    mcp = FastMCP("mail-ai-agent")

    mcp.add_tool(make_load_emails().run)
    mcp.add_tool(make_find_emails().run)

    return mcp

def run():
    make_mcp().run(
        transport=cast(Transport, getenv("MCP_BIND_TRANSPORT", "0.0.0.0")),
        host=getenv("MCP_BIND_HOST", "0.0.0.0"),
        port=int(getenv("MCP_BIND_PORT", 8000))
    )

if __name__ == "__main__":
    run()
