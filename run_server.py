import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

uvicorn.run(
    "doorway.api.server:app",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8000)),
)
