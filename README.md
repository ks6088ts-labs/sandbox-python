[![test](https://github.com/ks6088ts-labs/sandbox-python/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/sandbox-python/actions/workflows/test.yaml?query=branch%3Amain)
[![docker](https://github.com/ks6088ts-labs/sandbox-python/actions/workflows/docker.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/sandbox-python/actions/workflows/docker.yaml?query=branch%3Amain)
[![docker-release](https://github.com/ks6088ts-labs/sandbox-python/actions/workflows/docker-release.yaml/badge.svg)](https://github.com/ks6088ts-labs/sandbox-python/actions/workflows/docker-release.yaml)
[![ghcr-release](https://github.com/ks6088ts-labs/sandbox-python/actions/workflows/ghcr-release.yaml/badge.svg)](https://github.com/ks6088ts-labs/sandbox-python/actions/workflows/ghcr-release.yaml)

# sandbox-python

This is a template repository for Python

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [GNU Make](https://www.gnu.org/software/make/)

## Development instructions

### Local development

Use Makefile to run the project locally.

```shell
# help
make

# install dependencies for development
make install-deps-dev

# run tests
make test

# run CI tests
make ci-test
```

### Docker development

```shell
# build docker image
make docker-build

# run docker container
make docker-run

# run CI tests in docker container
make ci-test-docker
```

To publish the docker image to Docker Hub, you need to set the following secrets in the repository settings.

```shell
gh secret set DOCKERHUB_USERNAME --body $DOCKERHUB_USERNAME
gh secret set DOCKERHUB_TOKEN --body $DOCKERHUB_TOKEN
```

## scripts

### pdf_cli.py

```shell
# help
poetry run python scripts/pdf_cli.py --help

# Convert a PDF file to a Markdown file.
poetry run python scripts/pdf_cli.py pdf2md \
    --in-pdf "./datasets/sample.pdf" \
    --out-md "./datasets/sample.md" \
    --verbose

# Dump the table of contents (TOC) of a PDF file.
poetry run python scripts/pdf_cli.py toc \
    --in-pdf "./datasets/sample.pdf" \
    --verbose

# Dump tables of the specified page of a PDF file.
poetry run python scripts/pdf_cli.py tables \
    --in-pdf "./datasets/sample.pdf" \
    --page-number 123 \
    --verbose
```
