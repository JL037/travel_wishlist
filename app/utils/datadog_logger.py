# app/utils/datadog_logger.py

import os
from ddtrace import patch_all, tracer
from ddtrace.contrib.asgi import TraceMiddleware

# 🟢 Patch all supported libraries (like SQLAlchemy, etc.)
patch_all()

# 🟢 Datadog API key (ensure this is in Railway env)
DATADOG_API_KEY = os.getenv("DD_API_KEY")
if not DATADOG_API_KEY:
    raise Exception("Missing Datadog API Key!")

# 🟢 Set up tracer (Datadog uses this to send traces)
tracer.configure(
    hostname="https://trace.agent.datadoghq.com",  # Datadog APM endpoint
)

# 🟢 Use this middleware in your FastAPI app (see below)
datadog_middleware = TraceMiddleware
