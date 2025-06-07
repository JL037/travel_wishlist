# app/utils/datadog_logger.py

from ddtrace import patch_all
from ddtrace.contrib.asgi import TraceMiddleware

# 🟢 Patch all supported libraries (SQLAlchemy, requests, etc.)
patch_all()

# 🟢 Provide middleware to be added in main.py
datadog_middleware = TraceMiddleware
