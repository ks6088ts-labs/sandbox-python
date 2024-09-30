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

To support multimodal inputs, follow the instructions below:

- [How to pass multimodal data directly to models](https://python.langchain.com/docs/how_to/multimodal_inputs/)
- [How to use multimodal prompts](https://python.langchain.com/docs/how_to/multimodal_prompts/)
