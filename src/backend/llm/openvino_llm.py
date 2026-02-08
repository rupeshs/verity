import threading
from queue import Queue

import openvino_genai as ov_genai
from loguru import logger

from backend.llm.abstract_llm import AbstractLLM
from backend.llm.prompt import get_prompt
from backend.llm.question_generator import QuestionGeneratorMixin

MAX_PROMPT_LEN = 4096
MIN_RESPONSE_LEN = 128


class OpenvinoLLM(AbstractLLM, QuestionGeneratorMixin):
    def __init__(self, model: str, device="CPU"):
        self.model = model
        logger.info(f"⌛ Loading {model}...")
        if device.upper() == "NPU":
            pipeline_config = {
                "MAX_PROMPT_LEN": MAX_PROMPT_LEN,
                "NPUW_LLM_PREFILL_CHUNK_SIZE": MAX_PROMPT_LEN,
                "MIN_RESPONSE_LEN": MIN_RESPONSE_LEN,
            }
            self.pipe = ov_genai.LLMPipeline(
                model,
                device,
                pipeline_config,
            )
        else:
            self.pipe = ov_genai.LLMPipeline(model, device)
        logger.info(f"✅ Model loaded!")

    def _generate_ovstream(self, pipe, query, config):
        q = Queue()
        DONE = object()

        def streamer(token):
            q.put(token)
            return ov_genai.StreamingStatus.RUNNING

        def run():
            pipe.generate(query, config, streamer)
            q.put(DONE)

        threading.Thread(target=run, daemon=True).start()

        while True:
            token = q.get()
            if token is DONE:
                break
            yield {"message": {"content": token}}

    def get_answer_stream(self, context: str, question: str) -> any:
        prompt = get_prompt(context, question)
        stream = self.generate_stream(prompt)
        return stream

    def get_model(self) -> str:
        return self.model

    def generate_stream(self, prompt: str):
        config = ov_genai.GenerationConfig()
        config.max_new_tokens = 1024
        stream = self._generate_ovstream(self.pipe, prompt, config)
        return stream
