import os
import sys
import uvicorn

# Ensure the 'backend' directory is in Python's search path to handle app module imports.
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.config import settings

if __name__ == "__main__":
    # Start uvicorn server resolving 'app.main:app' relative to 'backend' directory
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=True
    )
