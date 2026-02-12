import os

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")

MAX_GET_RESPONSE_TIME_SEC = float(os.getenv("MAX_GET_RESPONSE_TIME_SEC", "1.0"))
MAX_POST_RESPONSE_TIME_SEC = float(os.getenv("MAX_POST_RESPONSE_TIME_SEC", "2.0"))

def api_base_url() -> str:
    return BASE_URL
