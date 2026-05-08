from fastapi import FastAPI
from config.settings import settings
from utils.exceptions import global_exception_handler
from routes import chat, health

def create_app() -> FastAPI:
    """
    Application factory pattern.
    Creates and configures the FastAPI application instance.
    """
    app = FastAPI(
        title=settings.app_name,
        description="Modular backend for an AI Recommendation System",
        version="1.0.0"
    )

    # Attach our centralized exception handler
    app.add_exception_handler(Exception, global_exception_handler)

    # Mount our modular routers
    # prefix="..." would go here if we wanted versioning like /api/v1/chat
    app.include_router(health.router, tags=["Health"])
    app.include_router(chat.router, tags=["Chat"])

    return app

# The main application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    # Allows running via `python main.py` directly
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
