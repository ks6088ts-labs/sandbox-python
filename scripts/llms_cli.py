import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from logging import getLogger

import typer

from sandbox_python.llms import core

app = typer.Typer()

logger = getLogger(__name__)


@app.command()
def create_vector_store(
    urls: list[str] = [
        "https://www.aozora.gr.jp/cards/000296/files/47061_29420.html",  # 学問のすすめ
    ],
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    verbose: bool = True,
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
    verbose: bool = False,
):
    if verbose:
        import logging

        logging.basicConfig(level=logging.DEBUG)

    got_documents = core.get_retriever(
        embedding=core.get_embedding(),
        collection_name=collection_name,
        persist_directory=persist_directory,
    ).invoke(query)

    print(f"got {len(got_documents)} documents")

    for idx, document in enumerate(got_documents):
        print(f"{idx+1} =============")
        print(document.page_content)


if __name__ == "__main__":
    app()
