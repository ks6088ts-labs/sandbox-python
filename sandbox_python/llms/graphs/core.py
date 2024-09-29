from enum import Enum
from typing import Any, TypedDict

from langchain_core.documents import Document
from langgraph.graph import END, StateGraph

from sandbox_python.llms.chains.core import rag_chain
from sandbox_python.llms.core import get_embedding, get_retriever
from sandbox_python.llms.tools.bing_search import get_bing_search_tool


class NodeType(Enum):
    RETRIEVE = "retrieve"
    SEARCH = "search"
    GENERATE = "generate"


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
        k: number of documents to retrieve
    """

    question: str
    generation: str
    web_search: bool
    documents: list[str]
    k: int


def retrieve(state: GraphState) -> dict[str, Any]:
    print("---RETRIEVE---")
    question = state["question"]
    k = state["k"]
    try:
        documents = state["documents"]
    except KeyError:
        documents = None

    retriever = get_retriever(
        embedding=get_embedding(),
        collection_name="rag-chroma",
        persist_directory="./.chroma",
        k=k,
    )
    got_documents = retriever.invoke(question)
    if documents is None:
        documents = got_documents
    else:
        documents.extend(got_documents)
    return {"documents": documents, "question": question}


def search(state: GraphState) -> dict[str, Any]:
    print("---SEARCH---")
    question = state["question"]
    documents = state["documents"]
    k = state["k"]

    got_documents_str = get_bing_search_tool(k=k).invoke(
        {
            "query": question,
        }
    )
    got_documents = [Document(page_content=document["snippet"]) for document in eval(got_documents_str)]
    if documents is None:
        documents = got_documents
    else:
        documents.extend(got_documents)
    return {"documents": documents, "question": question}


def generate(state: GraphState) -> dict[str, Any]:
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    generation = rag_chain.invoke({"context": documents, "question": question})
    return {"documents": documents, "question": question, "generation": generation}


def get_graph():
    workflow = StateGraph(GraphState)
    workflow.add_node(NodeType.RETRIEVE.value, retrieve)
    workflow.add_node(NodeType.SEARCH.value, search)
    workflow.add_node(NodeType.GENERATE.value, generate)

    workflow.set_entry_point(NodeType.RETRIEVE.value)
    workflow.add_edge(NodeType.RETRIEVE.value, NodeType.SEARCH.value)
    workflow.add_edge(NodeType.SEARCH.value, NodeType.GENERATE.value)
    workflow.add_edge(NodeType.GENERATE.value, END)

    return workflow.compile()
