import base64
import logging
import os
import sys
from logging import getLogger
from os import getenv
from pprint import pprint

import typer
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from line_profiler import profile as line_profile
from memory_profiler import profile as memory_profile
from openai import AzureOpenAI

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from sandbox_python.llms import core
from sandbox_python.llms.chains.core import rag_chain
from sandbox_python.llms.graphs.core import get_graph
from sandbox_python.llms.models.core import Joke
from sandbox_python.llms.tools.bing_search import get_bing_search_tool

app = typer.Typer()

logger = getLogger(__name__)

DEFAULT_URLS = [
    "https://www.aozora.gr.jp/cards/000296/files/47061_29420.html",  # 学問のすすめ
]


@app.command()
@line_profile
def create_vector_store(
    urls: list[str] = DEFAULT_URLS,
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    verbose: bool = typer.Option(True, help="Verbose mode."),
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
@line_profile
def search(
    query: str = "天は人の上に人を造らず人の下に人を造らず",
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    k: int = 3,
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
@line_profile
def bing_search(
    query: str = "GitHub",
    k: int = 3,
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
@line_profile
def rag(
    question="初版の発行日と出版社を教えてください。",
    vector_store=True,
    bing_search=True,
    k: int = 3,
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
@line_profile
def run_graph(
    question="初版の発行日と出版社を教えてください。",
    k: int = 1,
    image_file=None,  # specify image path to use image
    verbose: bool = typer.Option(False, help="Verbose mode."),
):
    if verbose:
        import logging

        logging.basicConfig(level=logging.DEBUG)

    images = None
    if image_file is not None:
        with open(image_file, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
            images = [image_data]

    for output in get_graph().stream(
        {
            "question": question,
            "k": k,
            "images": images,
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


@app.command()
@line_profile
def create_mermaid_png(
    output_mermaid_png: str = typer.Option("graph.png", help="Path to output mermaid png."),
    verbose: bool = typer.Option(False, help="Verbose mode."),
):
    if verbose:
        import logging

        logging.basicConfig(level=logging.DEBUG)

    get_graph().get_graph().draw_mermaid_png(output_file_path=output_mermaid_png)


# https://stackoverflow.com/questions/66193550/is-it-possible-to-run-memory-profiler-and-line-profiler-during-the-same-executio
@app.command()
@memory_profile
def create_mermaid_png_memory(
    output_mermaid_png: str = typer.Option("graph.png", help="Path to output mermaid png."),
    verbose: bool = typer.Option(False, help="Verbose mode."),
):
    if verbose:
        import logging

        logging.basicConfig(level=logging.DEBUG)

    get_graph().get_graph().draw_mermaid_png(output_file_path=output_mermaid_png)


@app.command()
@line_profile
def structured_output(
    verbose: bool = typer.Option(False, help="Verbose mode."),
):
    if verbose:
        import logging

        logging.basicConfig(level=logging.DEBUG)
    llm = core.get_chat_model()
    structured_llm = llm.with_structured_output(Joke)
    response: Joke = structured_llm.invoke("Tell me a joke")
    print(response.model_dump_json())


@app.command()
@line_profile
def structured_output_raw(
    verbose: bool = typer.Option(False, help="Verbose mode."),
):
    if verbose:
        import logging

        logging.basicConfig(level=logging.DEBUG)
    client = AzureOpenAI(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    )
    completion = client.beta.chat.completions.parse(
        model=getenv("AZURE_OPENAI_DEPLOYMENT_CHAT"),
        messages=[
            {"role": "user", "content": "Tell me a joke"},
        ],
        response_format=Joke,
    )
    event = completion.choices[0].message.parsed

    print(event)
    print(completion.model_dump_json(indent=2))


@app.command()
@line_profile
def create_knowledge_graph(
    urls: list[str] = DEFAULT_URLS,
    url="bolt://localhost:7687",
    username="neo4j",
    password="password",
    verbose: bool = typer.Option(False, help="Verbose mode."),
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Get chunked documents
    documents = core.get_text_splitter().split_documents(
        core.get_documents(
            urls=urls,
        )
    )
    # FIXME: Limit to 20 documents for now since it takes too long
    documents = documents[:20]

    # Extract graph data (heavy operation)
    graph_documents = LLMGraphTransformer(llm=core.get_chat_model()).convert_to_graph_documents(documents)

    # Store to neo4j
    Neo4jGraph(
        url=url,
        username=username,
        password=password,
    ).add_graph_documents(
        graph_documents,
        baseEntityLabel=True,
        include_source=True,
    )


if __name__ == "__main__":
    load_dotenv()

    app()
