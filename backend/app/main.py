from fastapi import FastAPI, Request
from .services.rag_engine import RAGEngine
from .utils.logger import logger
import os
from dotenv import load_dotenv
from .api import router
import time

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY no encontrada en las variables de entorno")

RAG_ENGINE = None

app = FastAPI(
    title="CoffeeBot API",
    description="Bot conversacional sobre café usando RAG + FastAPI",
    version="0.0.1",
)

# Middleware para loggear todas las requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"🔥 REQUEST: {request.method} {request.url}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"✅ RESPONSE: {response.status_code} - {process_time:.2f}s")
    return response

app.include_router(router)

@app.on_event("startup")
def startup_event():
    global RAG_ENGINE
    
    logger.info("Iniciando backend...")
    logger.info(f"API Key cargada: {GEMINI_API_KEY[:8]}...")
    pdf_path = os.path.join(os.path.dirname(__file__), "assets", "coffee-recipes.pdf")
    
    # Inicializar la instancia global
    RAG_ENGINE = RAGEngine(pdf_path=pdf_path)
    RAG_ENGINE.build_index()
    logger.info("RAG Engine listo y cargado.")

@app.get("/health")
def health_check():
    return {"status": "ok"}


