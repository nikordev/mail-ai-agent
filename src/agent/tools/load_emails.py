from email import message_from_bytes
from poplib import POP3, POP3_SSL

from fastmcp.tools import tool
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from src.agent.utils.core import make_email_document


class LoadMailsController:
    def __init__(
        self,
        ollama_url: str,
        pop3_host: str,
        pop3_port: int,
        pop3_user: str,
        pop3_pass: str,
        pop3_ssl: int,
        pop3_debug: int
    ):
        self.ollama_url = ollama_url
        self.pop3_host = pop3_host
        self.pop3_port = pop3_port
        self.pop3_user = pop3_user
        self.pop3_pass = pop3_pass
        self.pop3_ssl = pop3_ssl
        self.pop3_debug = pop3_debug

    @tool(
        name="load_emails",
        description="Load emails from SMTP server",
        tags={"emails", "load"},
    )
    def run(self) -> int:
        if self.pop3_ssl == 1:
            server = POP3_SSL(host=self.pop3_host, port=self.pop3_port)
        else:
            server = POP3(host=self.pop3_host, port=self.pop3_port)

        server.set_debuglevel(self.pop3_debug)
        server.user(self.pop3_user)
        server.pass_(self.pop3_pass)

        num_messages = len(server.list()[1])

        documents = []

        for i in range(num_messages, 0, -1):
            resp, lines, octets = server.top(i, 0)
            documents.append(make_email_document(
                message_from_bytes(b'\n'.join(lines))
            ))

        server.quit()

        embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url=self.ollama_url,
        )

        db = Chroma(
            persist_directory="/data/chroma",
            embedding_function=embeddings,
            collection_name="emails",
        )

        db.reset_collection()

        if len(documents) == 0:
            return 0

        db.add_documents(documents)

        return len(documents)
