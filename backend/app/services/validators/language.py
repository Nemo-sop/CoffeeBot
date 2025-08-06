from langdetect import detect
from ...utils.logger import logger

def is_spanish(text: str) -> bool:
    try:
        lang = detect(text)
        logger.debug(f"Idioma detectado: {lang}")
        return lang == "es"
    except Exception as e:
        logger.error(f"Error al detectar idioma: {e}")
        return False