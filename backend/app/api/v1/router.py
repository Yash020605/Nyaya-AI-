from fastapi import APIRouter
from app.api.v1 import research, drafting, admin, report, ml_retriever

api_router = APIRouter()

# 🟢 TYPE YOURSELF: Practice aggregating APIRouters in FastAPI.
# Uncomment or type the code below.
#
# Why this file exists: To consolidate all v1 endpoint sub-routers 
# (research, drafting, admin) under a unified namespace.
#
# Common mistake: Forgetting to register routers here, which leads to 
# "404 Not Found" when calling endpoints in frontend.
#
# How it will evolve: More features (e.g. users, authentication, audits)
# will be registered as separate routers as the app grows.

# Health Check router registered directly here
@api_router.get("/health",tags=["system"])
async def health_check():
    """
    System health check endpoint. Returns status of DBs and backend service.
    """
    return {
        "status": "healthy",
        "services": {
            "api": "online",
            "mongodb": "pending_connection",
            "qdrant": "pending_connection"
        }
    }

api_router.include_router(research.router, prefix="/research", tags=["research"])
api_router.include_router(drafting.router, prefix="/drafting", tags=["drafting"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(report.router, prefix="/report", tags=["report"])
api_router.include_router(ml_retriever.router, prefix="/ml-retriever", tags=["ml-retriever"])