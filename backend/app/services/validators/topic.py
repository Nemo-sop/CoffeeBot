from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from ...utils.logger import logger

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

COFFEE_REFERENCE_TEXT = "café, espresso, capuccino, latte, preparación de café, barista, recetas de café"
COFFEE_EMBEDDING = embedding_model.encode([COFFEE_REFERENCE_TEXT])[0]

def is_related_to_coffee(text: str, threshold: float = 0.33) -> bool:
    try:
        embedding = embedding_model.encode([text])[0]
        similarity = cosine_similarity([embedding], [COFFEE_EMBEDDING])[0][0]
        logger.info(f"Similaridad temática: {similarity:.3f}")
        return bool(similarity >= threshold)
    except Exception as e:
        logger.error(f"Error al evaluar tema café: {e}")
        return False
