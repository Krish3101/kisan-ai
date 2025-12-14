"""
Standardized API response utilities
"""
from typing import Any, Optional
from fastapi.responses import JSONResponse


def success_response(
    data: Any,
    message: str = "Success",
    status_code: int = 200
) -> JSONResponse:
    """Return standardized success response"""
    return JSONResponse(
        content={
            "success": True,
            "message": message,
            "data": data
        },
        status_code=status_code
    )


def error_response(
    message: str,
    error_code: Optional[str] = None,
    status_code: int = 400,
    details: Optional[dict] = None
) -> JSONResponse:
    """Return standardized error response"""
    content = {
        "success": False,
        "message": message,
    }
    
    if error_code:
        content["error_code"] = error_code
    
    if details:
        content["details"] = details
    
    return JSONResponse(
        content=content,
        status_code=status_code
    )
