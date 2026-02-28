import sys, os, traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Eager import so any error prints clearly before uvicorn's stack obscures it
try:
    from doorway.api.server import app
except Exception:
    traceback.print_exc()
    sys.exit(1)

import uvicorn

uvicorn.run(
    app,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8000)),
)
