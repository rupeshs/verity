import os

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openvino")
SEARXNG_BASE_URL = os.getenv("SEARXNG_BASE_URL", "http://localhost:8080")
DEVICE = os.getenv("DEVICE", "CPU")
NUM_SEARCH_RESULTS = int(os.getenv("NUM_SEARCH_RESULTS", 3))
LLM_MODEL_PATH = os.getenv("LLM_MODEL_PATH", "rupeshs/jan-nano-int4-ov")
API_PORT = int(os.getenv("API_PORT", 8000))
API_HOST = os.getenv("API_HOST", "0.0.0.0")
