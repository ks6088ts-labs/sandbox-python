from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from sandbox_python.llms.core import get_chat_model

llm = get_chat_model()

rag_chain = hub.pull("rlm/rag-prompt") | llm | StrOutputParser()

describe_image_chain = (
    ChatPromptTemplate.from_messages(
        [
            ("system", "Describe the image provided"),
            (
                "user",
                [
                    {
                        "type": "image_url",
                        "image_url": {"url": "data:image/jpeg;base64,{image_data}"},
                    }
                ],
            ),
        ]
    )
    | llm
    | StrOutputParser()
)
