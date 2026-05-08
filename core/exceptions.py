from fastapi import Request
from fastapi.responses import JSONResponse
from core.logger import logger

async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch-all exception handler to ensure the API never crashes completely
    and always returns a clean JSON response.
    """
    logger.error(f"Unhandled error processing request {request.method} {request.url}: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong on our end. Please try again later."
        }
    )
