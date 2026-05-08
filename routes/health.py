from fastapi import APIRouter
from models.schemas import APIResponse

router = APIRouter()

@router.get("/health", response_model=APIResponse[dict])
async def health_check():
    """
    A simple health check endpoint to verify the server is running.
    """
    return APIResponse(
        success=True,
        data={"status": "ok"},
        message="Server is healthy"
    )
