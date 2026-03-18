"""Request logging middleware."""
import time
import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("adp.api")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        start = time.time()

        logger.info(f"[{request_id}] {request.method} {request.url.path}")

        response = await call_next(request)

        duration_ms = round((time.time() - start) * 1000, 2)
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"-> {response.status_code} ({duration_ms}ms)"
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Duration-Ms"] = str(duration_ms)
        return response
