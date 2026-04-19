from fastmcp.tools import tool
from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings


class FindMailsController:
    def __init__(self, ollama_url: str):
        self.ollama_url = ollama_url

    @tool(
        name="find_emails",
        description="Search emails with text query",
        tags={"emails", "search"},
    )
    def run(self, query: str) -> str:
        embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url=self.ollama_url,
        )

        db = Chroma(
            persist_directory="/data/chroma",
            embedding_function=embeddings,
            collection_name="emails",
        )

        llm = Ollama(
            model="llama3",
            base_url=self.ollama_url,
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "\n".join((
                "You are an assistant for question-answering tasks.",
                "Use the following pieces of retrieved context to answer the question.",
                "If you don't know the answer, just say that you don't know.",
                "Use three sentences maximum and keep the answer concise:",
                "<context>",
                "{context}",
                "</context>"
            ))),
            ("placeholder", "{chat_history}"),
            ("human", "{input}")
        ])

        combine_docs_chain = create_stuff_documents_chain(llm, prompt)
        retrieval_chain = create_retrieval_chain(
            db.as_retriever(search_kwargs={"k": 10}),
            combine_docs_chain
        )

        response = retrieval_chain.invoke({"input": query})

        return response["answer"]
