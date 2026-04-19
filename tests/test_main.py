import uuid
from email.message import EmailMessage
from os import getenv
from smtplib import SMTP

import pytest
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from src.agent import make_mcp
from src.agent.utils.core import make_content_text


@pytest.fixture
async def main_mcp_client():
    async with Client(transport=make_mcp()) as mcp_client:
        yield mcp_client

@pytest.fixture
def smtp_client():
    server = SMTP(
        getenv("TEST_SMTP_HOST", "mail-ai-agent-mailpit-1"),
        int(getenv("TEST_SMTP_PORT", 1025))
    )
    server.login(str(uuid.uuid4()), str(uuid.uuid4()))
    return server

@pytest.fixture
def chroma_client():
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=getenv("OLLAMA_URL", "http://ollama:11434"),
    )

    return Chroma(
        persist_directory="/data/chroma",
        embedding_function=embeddings,
        collection_name="emails",
    )

async def test_list_tools(main_mcp_client: Client[FastMCPTransport]):
    list_tools = await main_mcp_client.list_tools()

    assert len(list_tools) == 2

async def test_find_emails(
        main_mcp_client: Client[FastMCPTransport],
        chroma_client: Chroma
):
    chroma_client.reset_collection()

    chroma_client.add_documents([
        Document(page_content=make_content_text(
            subject="do1",
            from_val="Unknown",
            to_val="Unknown",
            date="Unknown",
            content="ok1"
        )),
        Document(page_content=make_content_text(
            subject="do2",
            from_val="Unknown",
            to_val="Unknown",
            date="Unknown",
            content="ok2"
        )),
        Document(page_content=make_content_text(
            subject="do3",
            from_val="Unknown",
            to_val="Unknown",
            date="Unknown",
            content="ok3"
        ))
    ])

    result = await main_mcp_client.call_tool(
        name="find_emails", arguments={"query": "print integer count of 'ok'"}
    )

    assert "3" in result.data or "three" in result.data

    result = await main_mcp_client.call_tool(
        name="find_emails", arguments={"query": "print integer count of 'do' only"}
    )

    assert "3" in result.data or "three" in result.data

async def test_load_emails(
        main_mcp_client: Client[FastMCPTransport],
        smtp_client: SMTP,
        chroma_client: Chroma
):
    chroma_client.reset_collection()

    query=str(uuid.uuid4())

    search = chroma_client.search(
        query=query,
        search_type="similarity"
    )

    assert len(search) == 0

    result1 = await main_mcp_client.call_tool(name="load_emails")

    assert result1.data is not None

    msg = EmailMessage()
    msg['Subject'] = 'Test Email Subject'
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = 'pop3_user@example.com'
    msg.set_content(query)

    smtp_client.send_message(msg)

    result2 = await main_mcp_client.call_tool(name="load_emails")

    assert result2.data > result1.data

    result = await main_mcp_client.call_tool(
        name="find_emails",
        arguments={"query": f"print integer count of '{query}' only"}
    )

    assert "1" in result.data or "one" in result.data
