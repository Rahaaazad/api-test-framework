import requests
import time
from typing import Optional, Dict, Any

from .config import api_base_url, MAX_GET_RESPONSE_TIME_SEC, MAX_POST_RESPONSE_TIME_SEC
from .logger import get_logger

log = get_logger(__name__)


class APIClient:
    def __init__(self, timeout: float = 10.0):
        self.base_url = api_base_url()
        self.timeout = timeout
        self.session = requests.Session()

    def _check_performance(self, method: str, duration: float, limit_sec: float):
        assert duration <= limit_sec, (
            f"{method} response time too slow: {duration:.4f}s > {limit_sec:.2f}s"
        )

    def get(self, path: str, params: Optional[Dict[str, Any]] = None):
        url = f"{self.base_url}{path}"

        start_time = time.perf_counter()
        log.info("GET %s params=%s", url, params)

        r = self.session.get(url, params=params, timeout=self.timeout)

        duration = time.perf_counter() - start_time
        self._check_performance("GET", duration, MAX_GET_RESPONSE_TIME_SEC)

        log.info("Response status: %s | Duration: %.4f sec", r.status_code, duration)
        return r

    def post(self, path: str, json: Optional[Dict[str, Any]] = None):
        url = f"{self.base_url}{path}"

        start_time = time.perf_counter()
        log.info("POST %s json=%s", url, json)

        r = self.session.post(url, json=json, timeout=self.timeout)

        duration = time.perf_counter() - start_time
        self._check_performance("POST", duration, MAX_POST_RESPONSE_TIME_SEC)

        log.info("Response status: %s | Duration: %.4f sec", r.status_code, duration)
        return r
