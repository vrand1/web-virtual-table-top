from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.logs.errors import error_response
from loguru import logger

def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        request_id = getattr(request.state, 'request_id', None)
        
        logger.bind(request_id=request_id).error(f"HTTP Error: {exc.status_code} - {exc.detail}")

        return error_response(
            status_code=exc.status_code,
            request_id=request_id,
            code=f'http_{exc.status_code}',
            message=exc.detail if isinstance(exc.detail, str) else 'HTTP error',
            details=exc.detail
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        request_id = getattr(request.state, 'request_id', None)
        
        logger.bind(request_id=request_id, sink='console').warning("Validation failed")

        return error_response(
            status_code=422,
            request_id=request_id,
            code='validation_error',
            message='Request validation failed',
            details=exc.errors(),
        )