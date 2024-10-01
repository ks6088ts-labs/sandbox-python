from logging import getLogger

import onnxruntime_genai as og

logger = getLogger(__name__)


class SlmClient:
    def __init__(
        self,
        model_path=".onnx/cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4",
    ) -> None:
        logger.info(f"Loading model from {model_path}")
        self.model = og.Model(model_path)
        logger.info("Model loaded successfully.")
        self.tokenizer = og.Tokenizer(self.model)
        self.tokenizer_stream = self.tokenizer.create_stream()
        self.search_options = {}
        self.search_options["max_length"] = 2048
        self.chat_template = "<|user|>\n{input} <|end|>\n<|assistant|>"

    def invoke(self, input_text: str) -> str:
        logger.info(f"Invoking model with input: {input_text}")
        prompt = f"{self.chat_template.format(input=input_text)}"

        input_tokens = self.tokenizer.encode(prompt)

        params = og.GeneratorParams(self.model)
        params.set_search_options(**self.search_options)
        params.input_ids = input_tokens
        generator = og.Generator(self.model, params)

        response = ""
        while not generator.is_done():
            generator.compute_logits()
            generator.generate_next_token()

            new_token = generator.get_next_tokens()[0]
            decoded_token = self.tokenizer_stream.decode(new_token)
            logger.info(f"Decoded token: {decoded_token}")
            response += decoded_token
        del generator
        del params

        return response
