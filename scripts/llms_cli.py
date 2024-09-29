import os
import sys
from pprint import pprint

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from logging import getLogger

import typer
from dotenv import load_dotenv
from langchain_core.documents import Document

from sandbox_python.llms import core
from sandbox_python.llms.chains.core import rag_chain
from sandbox_python.llms.graphs.core import get_graph
from sandbox_python.llms.tools.bing_search import get_bing_search_tool

app = typer.Typer()

logger = getLogger(__name__)


@app.command()
def create_vector_store(
    urls: list[str] = [
        "https://www.aozora.gr.jp/cards/000296/files/47061_29420.html",  # 学問のすすめ
    ],
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    verbose: bool = typer.Option(False, help="Verbose mode."),
):
    if verbose:
        import logging

        logging.basicConfig(level=logging.DEBUG)

    documents = core.get_documents(
        urls=urls,
    )

    text_splitter = core.get_text_splitter()

    chunks = text_splitter.split_documents(documents)

    _ = core.create_vector_store(
        embedding=core.get_embedding(),
        documents=chunks,
        collection_name=collection_name,
        persist_directory=persist_directory,
    )


@app.command()
def search(
    query: str = "天は人の上に人を造らず人の下に人を造らず",
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    k=3,
    verbose: bool = typer.Option(False, help="Verbose mode."),
):
    if verbose:
        import logging

        logging.basicConfig(level=logging.DEBUG)

    got_documents = core.get_retriever(
        embedding=core.get_embedding(),
        collection_name=collection_name,
        persist_directory=persist_directory,
        k=k,
    ).invoke(query)

    print(f"got {len(got_documents)} documents")

    for idx, document in enumerate(got_documents):
        print(f"{idx+1} =============")
        pprint(document)


@app.command()
def bing_search(
    query: str = "GitHub",
    k=3,
    verbose: bool = typer.Option(False, help="Verbose mode."),
):
    if verbose:
        import logging

        logging.basicConfig(level=logging.DEBUG)

    documents_str = get_bing_search_tool(k=k).invoke(
        {
            "query": query,
        }
    )
    documents = eval(documents_str)

    for idx, document in enumerate(documents):
        print(f"{idx+1} =============")
        pprint(document)


@app.command()
def rag(
    question="初版の発行日と出版社を教えてください。",
    vector_store=True,
    bing_search=True,
    k=3,
    verbose: bool = typer.Option(False, help="Verbose mode."),
):
    if verbose:
        import logging

        logging.basicConfig(level=logging.DEBUG)

    documents = []
    if vector_store:
        got_documents = core.get_retriever(
            embedding=core.get_embedding(),
            collection_name="rag-chroma",
            persist_directory="./.chroma",
            k=k,
        ).invoke(question)
        documents.extend(got_documents)

    if bing_search:
        got_documents_str = get_bing_search_tool(k=k).invoke(
            {
                "query": question,
            }
        )
        got_documents = eval(got_documents_str)
        for document in got_documents:
            documents.append(Document(page_content=document["snippet"]))

    for idx, document in enumerate(documents):
        print(f"{idx+1} =============")
        pprint(document)

    generation = rag_chain.invoke(
        {
            "context": documents,
            "question": question,
        }
    )

    print("Answer =============")
    pprint(generation)


@app.command()
def agent(
    question="初版の発行日と出版社を教えてください。",
    output_mermaid_png=None,
    k=3,
    verbose: bool = typer.Option(False, help="Verbose mode."),
):
    if verbose:
        import logging

        logging.basicConfig(level=logging.DEBUG)

    graph = get_graph()
    graph.get_graph().draw_mermaid_png(output_file_path=output_mermaid_png)

    for output in graph.stream(
        {
            "question": question,
            "k": k,
        },
        config={
            "configurable": {
                "thread_id": "2",
            }
        },
    ):
        for key, value in output.items():
            pprint(f"Finished running: {key}:")
    pprint(value["generation"])


if __name__ == "__main__":
    load_dotenv()

    app()
