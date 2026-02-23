from typing import Any, Optional
from fastapi.responses import JSONResponse

def error_payload(
    *,
    request_id: Optional[str],
    code: str,
    message: str,
    details: Any | None = None,
) -> dict:
    payload = {
        "error": {
            "code": code,
            "message": message,
            "request_id": request_id,
        }
    }
    if details is not None:
        payload["error"]["details"] = details
    return payload

def error_response(
    *,
    status_code: int,
    request_id: Optional[str],
    code: str,
    message: str,
    details: Any | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=error_payload(
            request_id=request_id, code=code, message=message, details=details
        ),
    )