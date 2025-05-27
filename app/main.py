from fastapi import FastAPI
from app.routers import wishlist, auth
from fastapi.openapi.utils import get_openapi

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel Wishlist API!"}


app.include_router(wishlist.router)
app.include_router(auth.router)


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
