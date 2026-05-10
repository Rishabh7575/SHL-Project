from fastapi import FastAPI
from config.settings import settings
from utils.exceptions import global_exception_handler
from routes import chat, health

def create_app() -> FastAPI:
    """Create the FastAPI app instance."""
    app = FastAPI(
        title=settings.app_name,
        description="AI Recommendation System Backend",
        version="1.0.0"
    )

    app.add_exception_handler(Exception, global_exception_handler)

    app.include_router(health.router, tags=["Health"])
    app.include_router(chat.router, tags=["Chat"])

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
