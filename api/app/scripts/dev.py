"""
Development server startup script.
Configures and runs the FastAPI application with hot reload.
"""

import uvicorn

from app.core.config.settings import get_settings


def main() -> None:
    """
    Start the development server.

    This function is called when running 'uv run dev' as configured
    in pyproject.toml under [project.scripts].
    """
    settings = get_settings()

    print(f"🚀 Starting {settings.project_name} v{settings.project_version}")
    print(f"🌐 Server will be available at: http://{settings.host}:{settings.port}")
    print(f"📚 API documentation: http://{settings.host}:{settings.port}/docs")
    print(f"📖 ReDoc documentation: http://{settings.host}:{settings.port}/redoc")
    print(f"🔧 Debug mode: {settings.debug}")

    # Configure uvicorn for development
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        reload_dirs=["app"] if settings.debug else None,
        log_level=settings.log_level.lower(),
        access_log=settings.debug,
        use_colors=True,
    )


if __name__ == "__main__":
    main()
