import os
import google.generativeai as genai
from .base import LLMBase
from ...utils.logger import logger
from ...utils.token_counter import log_token_usage

class GeminiLLM(LLMBase):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no encontrado en variables de entorno.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        logger.info(f"{self.model} inicializado.")

    def generate_answer(self, question: str, context: str, retries: int) -> str:
        prompt = (
            f"Eres un experto en café y estás respondiendo en español, hace que tu respuesta sea corta y concisa.\n"
            f"Si el usuario te pregunta sobreun cafe en particular, responde con un resumen de la receta de la bebida que te pide el usuario.\n"
            f"seed: {retries}\n" #para evitar el cacheo en gemini y poder reintentar la respuesta
            f"Pregunta: {question}\n"
            f"Contexto relevante:\n{context}\n"
            f"Respuesta:"
        )
        
        # Monitorear uso de tokens
        total_tokens = log_token_usage(prompt, context)
        
        try:
            response = self.model.generate_content(prompt)
            answer = response.text.strip()
            logger.debug(f"Respuesta generada: {answer}")
            return answer
        except Exception as e:
            logger.error(f"Error al invocar Gemini: {e}")
            return "Lo siento, hubo un error al generar la respuesta."
