from logging import getLogger
from os import getenv

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters.base import TextSplitter

load_dotenv()

logger = getLogger(__name__)


def get_embedding() -> Embeddings:
    return AzureOpenAIEmbeddings(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
        model=getenv("AZURE_OPENAI_DEPLOYMENT_EMBEDDING"),
    )


def get_retriever(
    embedding: Embeddings,
    collection_name: str,
    persist_directory: str,
) -> VectorStoreRetriever:
    return Chroma(
        collection_name=collection_name,
        persist_directory=persist_directory,
        embedding_function=embedding,
    ).as_retriever()


def get_text_splitter() -> TextSplitter:
    return RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=2**10,
        chunk_overlap=0,
    )


def get_documents(urls: list[str]) -> list[Document]:
    docs = [WebBaseLoader(url).load() for url in urls]
    return [item for sublist in docs for item in sublist]


def create_vector_store(
    embedding: Embeddings,
    documents: list[Document],
    collection_name: str,
    persist_directory: str,
) -> VectorStore:
    return Chroma.from_documents(
        documents=documents,
        collection_name=collection_name,
        persist_directory=persist_directory,
        embedding=embedding,
    )
