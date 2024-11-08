import logging
import pathlib

import pymupdf
import pymupdf4llm
import typer

app = typer.Typer(
    add_completion=False,
)

logger = logging.getLogger(__name__)


@app.command(
    help="Convert a PDF file to a Markdown file.",
)
def pdf2md(
    in_pdf: str = typer.Option(..., help="Path to the input PDF file."),
    out_md: str = typer.Option(..., help="Path to the output Markdown file."),
    verbose: bool = typer.Option(True, help="Verbose mode."),
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    try:
        logger.info(f"Converting {in_pdf} to {out_md}")
        md_text = pymupdf4llm.to_markdown(
            doc=in_pdf,
        )
        pathlib.Path(out_md).write_bytes(md_text.encode())
    except Exception as e:
        logger.error(e)


@app.command(
    help="Dump the table of contents (TOC) of a PDF file.",
)
def toc(
    in_pdf: str = typer.Option(..., help="Path to the input PDF file."),
    verbose: bool = typer.Option(True, help="Verbose mode."),
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    try:
        doc = pymupdf.open(in_pdf)
        # https://pymupdf.readthedocs.io/en/latest/document.html#Document.get_toc
        toc = doc.get_toc()
        for i, (level, title, page) in enumerate(toc):
            logger.info(f"{i}: {level}, {title}, {page}")
    except Exception as e:
        logger.error(e)


@app.command(
    help="Dump tables of the specified page of a PDF file.",
)
def tables(
    in_pdf: str = typer.Option(..., help="Path to the input PDF file."),
    page_number: int = typer.Option(0, help="Page number."),
    verbose: bool = typer.Option(True, help="Verbose mode."),
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    try:
        doc = pymupdf.open(in_pdf)
        page = doc[page_number - 1]  # 0-based index
        # https://pymupdf.readthedocs.io/en/latest/page.html#Page.find_tables
        tables = page.find_tables()
        for i, table in enumerate(tables):
            logger.info(f"Table {i}: {table.to_markdown()}")
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    app()
