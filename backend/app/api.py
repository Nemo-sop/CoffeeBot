from fastapi import APIRouter
from .models.schemas import UserQuery, BotResponse
from .services.validators.language import is_spanish
from .services.validators.topic import is_related_to_coffee
from .utils.logger import logger

router = APIRouter()
# Inicialización perezosa para LLM
llm = None

def get_llm():
    global llm
    if llm is None:
        from .services.llm.gemini_wrapper import GeminiLLM
        llm = GeminiLLM()
    return llm

@router.post("/ping", response_model=BotResponse)
def ping():
    return BotResponse(answer="Conection with Backend successful", retries=0)

@router.post("/ask", response_model=BotResponse)
def ask_question(query: UserQuery):
    # Importar RAG_ENGINE del módulo main
    from .main import RAG_ENGINE
    
    logger.info(f"-- Pregunta recibida: {query.question}")
    
    if not is_spanish(query.question):
        return BotResponse(answer="Solo hablo español.", retries=0)

    conversation_history = "\n".join(query.history)
    full_question = f"{conversation_history}\nUsuario: {query.question}"
    context = "\n\n".join(RAG_ENGINE.query(query.question))
    logger.info(f"Contexto a utilizar: {context}")
    retries = 0
    max_retries = 3

    while retries < max_retries:
        answer = get_llm().generate_answer(full_question, context, retries)
        logger.info(f"Respuesta {retries + 1}: {answer}")
        if is_spanish(answer) and is_related_to_coffee(answer):
            logger.info("[OK] Respuesta válida.")
            return BotResponse(answer=answer, retries=retries)
        
        logger.warning(f"[RETRY] Respuesta inválida. Reintentando... ({retries + 1})")
        retries += 1

    logger.error("[ERROR] No se pudo generar respuesta válida tras múltiples intentos.")
    return BotResponse(answer="Lo siento, estamos teniendo problemas para responder esa pregunta. Intenta nuevamente.", retries=retries)
