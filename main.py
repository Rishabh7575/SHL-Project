from fastapi import FastAPI
from api.routes import router as api_router
from core.config import settings
from core.exceptions import global_exception_handler

def create_app() -> FastAPI:
    # Initialize the FastAPI app
    app = FastAPI(
        title=settings.app_name,
        description="A simple, modular backend for an AI Recommendation System",
        version="1.0.0"
    )

    # Register the centralized exception handler
    app.add_exception_handler(Exception, global_exception_handler)

    # Include all API routes
    app.include_router(api_router)

    return app

# The actual app instance run by uvicorn
app = create_app()

if __name__ == "__main__":
    import uvicorn
    # This allows running the app directly via `python main.py` for debugging
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
