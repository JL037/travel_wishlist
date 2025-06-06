import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from app.core.config import settings
from fastapi import FastAPI
from app.routers import wishlist, auth, visited, weather, user_saved_cities, travel_plans
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from app.utils.limiter import Limiter

sentry_sdk.init(
    dsn= settings.SENTRY_DSN,  # 🟡 Replace this with the real DSN from Sentry dashboard!
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,  # 🟡 Performance tracing (1.0 = 100%, lower this in production!)
    environment="development",  # or
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://travel-wishlist-zeta.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)

app.add_middleware(SlowAPIMiddleware)

app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)



@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel Wishlist API!"}




app.include_router(wishlist.router)
app.include_router(auth.router)
app.include_router(visited.router)
app.include_router(weather.router, prefix="/api")
app.include_router(user_saved_cities.router, prefix="/api", tags=["user-saved-cities"])
app.include_router(travel_plans.router, prefix="/api")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Travel Wishlist API",
        version="1.0.0",
        description="Track places you want to visit and those you already have.",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
