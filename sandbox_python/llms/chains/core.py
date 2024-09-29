from langchain import hub
from langchain_core.output_parsers import StrOutputParser

from sandbox_python.llms.core import get_chat_model

llm = get_chat_model()
rag_prompt = hub.pull("rlm/rag-prompt")

rag_chain = rag_prompt | llm | StrOutputParser()
