import json
import time
import traceback
import uuid
from pathlib import Path
from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

def _pick_location(exc: BaseException) -> str:
    tb = traceback.extract_tb(exc.__traceback__)
    if not tb:
        return 'unknown'
    for frame in reversed(tb):
        p = frame.filename.replace('\\', '/')
        if '/backend/' in p or '/src/' in p:
            return f'{Path(frame.filename).name}:{frame.lineno} ({frame.name})'
    last = tb[-1]
    return f'{Path(last.filename).name}:{last.lineno} ({last.name})'

async def _decode_body(request: Request):
    body_bytes = await request.body()
    if not body_bytes:
        return None
    try:
        body_text = body_bytes[:4096].decode("utf-8", errors="replace")
        if "application/json" in request.headers.get("content-type", ""):
            return json.loads(body_text)
        return body_text
    except:  # noqa: E722
        return f"<{len(body_bytes)} bytes>"

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in {"/metrics", "/openapi.json", "/docs"}:
            return await call_next(request)

        req_body = await _decode_body(request)
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        logger.bind(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            request_body=req_body
        ).info(f'REQUEST: {request.method} {request.url.path}')

        start_time = time.perf_counter()
        try:
            response = await call_next(request)
            duration = (time.perf_counter() - start_time) * 1000
            
            log = logger.bind(request_id=request_id, status_code=response.status_code)
            if 200 <= response.status_code < 300:
                log.success(f'RESPONSE: {request.method} {request.url.path} [{response.status_code}] {duration:.2f}ms')
            elif 400 <= response.status_code < 500:
                
                log.warning(f'RESPONSE: {request.method} {request.url.path} [{response.status_code}] {duration:.2f}ms')
            else:
                log.error(f'RESPONSE: {request.method} {request.url.path} [{response.status_code}] {duration:.2f}ms')
            
            response.headers['X-Request-ID'] = request_id
            return response

        except Exception as exc:
            duration = (time.perf_counter() - start_time) * 1000
            location = _pick_location(exc)
            
            status_code = 500
            error_code = "internal_server_error"
            
            if "Unauthorized" in type(exc).__name__ or status_code == 401:
                status_code = 401
                error_code = "unauthorized"
            elif "ValidationError" in type(exc).__name__:
                status_code = 422
                error_code = "validation_error"

            log_msg = f'CRASH: {type(exc).__name__}: {str(exc)} at {location}'
            
            log_bind = logger.bind(
                request_id=request_id,
                location=location,
                duration_ms=round(duration, 2)
            )
            
            if status_code >= 500:
                log_bind.error(log_msg)
            else:
                log_bind.warning(log_msg)

            return JSONResponse(
                status_code=status_code,
                content={
                    'detail': str(exc) if status_code != 500 else 'Internal server error',
                    'request_id': request_id,
                    'code': error_code
                }
            )