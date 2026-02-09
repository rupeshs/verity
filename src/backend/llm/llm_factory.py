from huggingface_hub import snapshot_download
from backend.llm.util import is_local_path
from loguru import logger


class LLMFactory:
    @staticmethod
    def create_llm(
        llm_provider: str,
        model_path_or_name: str,
        device: str = "CPU",
        api_base_url: str = None,
        api_key: str = None,
    ):
        logger.info(f"LLM Provider: {llm_provider}")
        if llm_provider.lower() == "ollama":
            from backend.llm.ollama_llm import OllamaLLM

            return OllamaLLM(model=model_path_or_name)
        elif llm_provider.lower() == "openvino":
            from backend.llm.openvino_llm import OpenvinoLLM

            if is_local_path(model_path_or_name):
                model_path = model_path_or_name
            else:
                model_path = snapshot_download(
                    repo_id=model_path_or_name, repo_type="model"
                )
            return OpenvinoLLM(model=model_path, device=device)
        elif llm_provider.lower() == "openai":
            from backend.llm.openai_compatible_llm import OpenAICompatibleLLM

            return OpenAICompatibleLLM(
                model=model_path_or_name,
                base_url=api_base_url,
                api_key=api_key,
            )
        else:
            raise Exception(
                "Error: LLM Provider not yet supported! please use one of the following: openvino, ollama"
            )
