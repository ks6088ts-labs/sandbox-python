# References

## Azure Functions

Run the function app locally

```shell
# Run the function app locally with the Azure Functions Core Tools
$ poetry run func start
```

Deploy the function app to Azure

```shell
# Deploy resources to Azure
$ bash scripts/deploy_azure_functions_resources.sh

# Export dependencies to requirements.txt
$ poetry export -f requirements.txt -o requirements.txt --without-hashes

# Deploy the function app
$ func azure functionapp publish $FUNCTION_APP_NAME
```

### References

- [Using FastAPI Framework with Azure Functions](https://learn.microsoft.com/en-us/samples/azure-samples/fastapi-on-azure-functions/fastapi-on-azure-functions/)

## Streamlit

```shell
$ poetry run python -m streamlit run sandbox_python/streamlits/main.py
```

## LangChain

To return structured data from a model, follow the instructions below:

- [MS Learn > Structured outputs](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/structured-outputs?tabs=python)
- [How to return structured data from a model](https://python.langchain.com/docs/how_to/structured_output/)

To support multimodal inputs, follow the instructions below:

- [How to pass multimodal data directly to models](https://python.langchain.com/docs/how_to/multimodal_inputs/)
- [How to use multimodal prompts](https://python.langchain.com/docs/how_to/multimodal_prompts/)

## Graph RAG

To create a knowledge graph database, follow the instructions below:

```shell
# Start the Neo4j database
$ docker compose up

# Create indexes and constraints
$ poetry run python scripts/llms_cli.py create-knowledge-graph --verbose
```

After creating the knowledge graph, access the Neo4j browser at `http://localhost:7474` and you can query it using the following command:

```
// Get some data
MATCH (n1)-[r]->(n2) RETURN r, n1, n2 LIMIT 25
```

![Graph RAG](./images/visualize_graph_database.png)

### References

- [LangChain > Neo4j](https://python.langchain.com/docs/integrations/providers/neo4j/)
- [Enhancing RAG-based application accuracy by constructing and leveraging knowledge graphs](https://blog.langchain.dev/enhancing-rag-based-applications-accuracy-by-constructing-and-leveraging-knowledge-graphs/)
- [llm/enhancing_rag_with_graph.ipynb](https://github.com/tomasonjo/blogs/blob/master/llm/enhancing_rag_with_graph.ipynb?ref=blog.langchain.dev)
- [LangChain Neo4j Integration](https://neo4j.com/labs/genai-ecosystem/langchain/)

## ONNX runtime

```shell
# Download the model
$ poetry run huggingface-cli download microsoft/Phi-3-mini-4k-instruct-onnx \
    --include "cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4/*" \
    --local-dir .onnx/

# Run the model
$ poetry run python scripts/slms_cli.py run-slm --verbose
```

### References

- [microsoft/onnxruntime-genai](https://github.com/microsoft/onnxruntime-genai)
