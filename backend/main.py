from fastapi import FastAPI, APIRouter
from src.modules.ws.router import router as ws_router
from src.modules.auth.router import router as auth_router
from src.test.router import router as test_router
from src.logs.logging import setup_logging  
from src.logs.handlers import setup_exception_handlers 
from src.logs.middleware import LoggingMiddleware

setup_logging()

app = FastAPI(
    title="WebTTS",
    description="API для WebTTS",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(ws_router, prefix="/ws", tags=["WebSocket"])
api_v1_router.include_router(auth_router, prefix="", tags=["Auth"])
api_v1_router.include_router(test_router, prefix="/test", tags=["Test"])
    
app.include_router(api_v1_router)

app.add_middleware(LoggingMiddleware)
setup_exception_handlers(app)