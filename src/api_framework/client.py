import requests
import time
from typing import Optional, Dict, Any

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .config import api_base_url, MAX_GET_RESPONSE_TIME_SEC, MAX_POST_RESPONSE_TIME_SEC
from .logger import get_logger

log = get_logger(__name__)


class RetryableStatusCodeError(Exception):
    def __init__(self, status_code: int, url: str):
        super().__init__(f"Retryable HTTP status {status_code} for {url}")
        self.status_code = status_code
        self.url = url


class APIClient:
    
    RETRY_STATUS_CODES = {429, 500, 502, 503, 504}

    def __init__(self, timeout: float = 10.0, max_attempts: int = 3):
        self.base_url = api_base_url()
        self.timeout = timeout
        self.session = requests.Session()
        self.max_attempts = max_attempts

    def _check_performance(self, method: str, duration: float, limit_sec: float):
        assert duration <= limit_sec, (
            f"{method} response time too slow: {duration:.4f}s > {limit_sec:.2f}s"
        )

    def _build_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _should_retry_status(self, status_code: int) -> bool:
        return status_code in self.RETRY_STATUS_CODES

    def _request_with_retry(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        
        """

        
        @retry(
            stop=stop_after_attempt(self.max_attempts),
            wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
            retry=retry_if_exception_type(
                (requests.exceptions.Timeout,
                 requests.exceptions.ConnectionError,
                 RetryableStatusCodeError)
            ),
            reraise=True,
        )
        def _do() -> requests.Response:
            log.info("%s %s kwargs=%s", method, url, {k: v for k, v in kwargs.items() if k != "json"})

            r = self.session.request(method, url, timeout=self.timeout, **kwargs)

            if self._should_retry_status(r.status_code):
                
                raise RetryableStatusCodeError(r.status_code, url)

            return r

        return _do()

    def get(self, path: str, params: Optional[Dict[str, Any]] = None):
        url = self._build_url(path)

        start_time = time.perf_counter()
        try:
            r = self._request_with_retry("GET", url, params=params)
        except RetryableStatusCodeError as e:
           
            log.info("Final failure after retries: %s", str(e))
            raise

        duration = time.perf_counter() - start_time

        self._check_performance("GET", duration, MAX_GET_RESPONSE_TIME_SEC)

        log.info("Response status: %s | Total duration: %.4f sec", r.status_code, duration)
        return r

    def post(self, path: str, json: Optional[Dict[str, Any]] = None):
        url = self._build_url(path)

        start_time = time.perf_counter()
        try:
            r = self._request_with_retry("POST", url, json=json)
        except RetryableStatusCodeError as e:
            log.info("Final failure after retries: %s", str(e))
            raise

        duration = time.perf_counter() - start_time

        self._check_performance("POST", duration, MAX_POST_RESPONSE_TIME_SEC)

        log.info("Response status: %s | Total duration: %.4f sec", r.status_code, duration)
        return r
