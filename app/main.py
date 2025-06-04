import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from app.core.config import settings

sentry_sdk.init(
    dsn= settings.SENTRY_DSN,  # 🟡 Replace this with the real DSN from Sentry dashboard!
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,  # 🟡 Performance tracing (1.0 = 100%, lower this in production!)
    environment="development",  # or
)
from fastapi import FastAPI
from app.routers import wishlist, auth, visited, weather, user_saved_cities, travel_plans
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel Wishlist API!"}

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0  # This will intentionally crash!



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
