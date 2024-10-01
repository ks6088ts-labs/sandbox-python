import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import logging
from logging import getLogger

import typer
from dotenv import load_dotenv

from sandbox_python.slms.core import SlmClient

app = typer.Typer()

logger = getLogger(__name__)


@app.command()
def run_slm(
    model_path: str = typer.Option(
        ".onnx/cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4",
        help="Path to the SLM model.",
    ),
    verbose: bool = typer.Option(False, help="Verbose mode."),
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    client = SlmClient(model_path=model_path)
    try:
        while True:
            message = input("Enter message: ")
            result = client.invoke(message)
            print(result)
    except KeyboardInterrupt:
        print("Ctrl+C pressed, aborting generation")


@app.command()
def sandbox(
    verbose: bool = typer.Option(False, help="Verbose mode."),
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    logger.info("Running sandbox")


if __name__ == "__main__":
    load_dotenv()
    app()
