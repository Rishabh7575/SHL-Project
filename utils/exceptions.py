from fastapi import Request
from fastapi.responses import JSONResponse
from utils.logger import logger

async def global_exception_handler(request: Request, exc: Exception):
    """
    Catches any unhandled errors in our app.
    Prevents the server from crashing and returns a standardized, user-friendly JSON response.
    """
    logger.error(f"Unhandled error on {request.method} {request.url}: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal Server Error",
            "message": "Something went wrong on our end."
        }
    )
