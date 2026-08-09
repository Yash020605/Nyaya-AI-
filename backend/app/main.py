from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router

# 🟢 TYPE YOURSELF: Practice initializing a FastAPI application.
# Uncomment or type the code below.
#
# Why this file exists: Entrypoint of the FastAPI app. Configures 
# CORS (for frontend access), registers routes, and boots the uvicorn server.
#
# Common mistake: Misordering middleware registration or router inclusion.
# Router inclusion should generally happen after middleware setups.
#
# How it will evolve: Later we can add database startup/shutdown lifespan 
# handlers (to connect/disconnect MongoDB and Qdrant clients gracefully).

app = FastAPI(
    title = settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# # Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to the NyayaAI API. Access /docs for interactive documentation."}
