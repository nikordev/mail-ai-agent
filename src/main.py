from os import getenv

from fastmcp import FastMCP

from tools.find_emails import FindMailsController
from tools.load_emails import LoadMailsController

mcp = FastMCP("mail-ai-agent")

ollama_url = getenv("OLLAMA_URL", "http://ollama:11434")

load_emails = LoadMailsController(
    ollama_url=ollama_url,
    pop3_host=getenv("POP3_HOST", "mail-ai-agent-mailpit-1"),
    pop3_port=int(getenv("POP3_PORT", 1110)),
    pop3_user=getenv("POP3_USER", "user"),
    pop3_pass=getenv("POP3_PASS", "password"),
    pop3_ssl=int(getenv("POP3_SSL", 0))
)
mcp.add_tool(load_emails.run)

find_emails = FindMailsController(
    ollama_url=ollama_url
)
mcp.add_tool(find_emails.run)

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host=getenv("MCP_BIND_HOST", "0.0.0.0"),
        port=int(getenv("MCP_BIND_PORT", 8000))
    )
