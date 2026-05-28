import os as OS
from dotenv import load_dotenv

load_dotenv()

MAX_TOOL_CALLS = 5
LLM_MODEL = "z-ai/glm-4.5-air:free"
MAX_TOKENS = 1_000
TEMPERATURE = 0.7
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MAX_CONTEXT_LENGTH = 131_000
COMPACTION_THRESHOLD = 0.9
COMPACTION_RECENT_N = 5

HEADERS = {
    "Authorization": f"Bearer {OS.getenv('OPENROUTER_API_KEY')}",
    "Content-Type": "application/json",
}

BASIC_PAYLOAD = {
    "model": LLM_MODEL,
    "max_tokens": MAX_TOKENS,
    "temperature": TEMPERATURE,
}
