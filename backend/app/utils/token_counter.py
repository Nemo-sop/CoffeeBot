from typing import List
from .logger import logger

def estimate_tokens(text: str) -> int:
    """
    Estima el número de tokens basado en caracteres.
    Regla general: 1 token ≈ 4 caracteres
    """
    return len(text) // 4

def estimate_tokens_from_context(context_chunks: List[str]) -> int:
    """Calcula tokens totales de una lista de chunks de contexto"""
    total_chars = sum(len(chunk) for chunk in context_chunks)
    return total_chars // 4

def optimize_context_for_tokens(context_chunks: List[str], max_tokens: int = 3000) -> List[str]:
    """
    Optimiza el contexto para no exceder un límite de tokens.
    Prioriza los primeros chunks (más relevantes) y recorta si es necesario.
    """
    optimized_chunks = []
    current_tokens = 0
    
    for chunk in context_chunks:
        chunk_tokens = estimate_tokens(chunk)
        
        if current_tokens + chunk_tokens <= max_tokens:
            # El chunk completo cabe
            optimized_chunks.append(chunk)
            current_tokens += chunk_tokens
        else:
            # Calcular cuántos caracteres podemos usar del chunk actual
            remaining_tokens = max_tokens - current_tokens
            remaining_chars = remaining_tokens * 4
            
            if remaining_chars > 100:  # Solo agregar si queda espacio significativo
                truncated_chunk = chunk[:remaining_chars] + "..."
                optimized_chunks.append(truncated_chunk)
                logger.warning(f"Chunk truncado: {chunk_tokens} → {remaining_tokens} tokens")
            
            break  # No procesar más chunks
    
    final_tokens = estimate_tokens_from_context(optimized_chunks)
    logger.info(f"Contexto optimizado: {len(context_chunks)} → {len(optimized_chunks)} chunks, ~{final_tokens} tokens")
    
    return optimized_chunks

def log_token_usage(prompt: str, context: str):
    """Registra el uso de tokens para monitoreo"""
    prompt_tokens = estimate_tokens(prompt)
    context_tokens = estimate_tokens(context)
    total_tokens = prompt_tokens + context_tokens
    
    logger.info(f"📊 Uso de tokens - Prompt: ~{prompt_tokens}, Contexto: ~{context_tokens}, Total: ~{total_tokens}")
    
    # Alertas si el uso es alto
    if total_tokens > 4000:
        logger.warning(f"⚠️  Alto uso de tokens: {total_tokens} (considerar optimización)")
    elif total_tokens > 6000:
        logger.error(f"🚨 Uso crítico de tokens: {total_tokens} (puede exceder límites)")
    
    return total_tokens 