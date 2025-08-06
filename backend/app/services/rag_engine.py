import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from ..utils.pdf_loader import extract_pages_from_pdf
from ..utils.token_counter import estimate_tokens_from_context, optimize_context_for_tokens
from ..utils.logger import logger
import os
from typing import List

class RAGEngine:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.text_chunks: List[str] = []
        self.embeddings = None

    def build_index(self):
        logger.info("Construyendo índice FAISS con páginas como chunks...")
        
        # Extraer páginas directamente (cada página = 1 chunk)
        self.text_chunks = extract_pages_from_pdf(self.pdf_path)
        
        if not self.text_chunks:
            raise ValueError("No se pudieron extraer páginas del PDF")
            
        logger.info(f"Usando {len(self.text_chunks)} páginas como chunks")
        
        # Crear embeddings para cada página
        self.embeddings = self.embedding_model.encode(self.text_chunks, show_progress_bar=True)
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(self.embeddings).astype('float32'))
        logger.info(f"FAISS index creado con {len(self.text_chunks)} páginas.")

    def query(self, question: str, top_k: int = 2) -> List[str]:
        question_vec = self.embedding_model.encode([question])
        D, I = self.index.search(np.array(question_vec).astype('float32'), top_k)
        
        relevant_pages = [self.text_chunks[i] for i in I[0]]
        logger.debug(f"Query: '{question}' → {len(relevant_pages)} páginas encontradas")
        
        return relevant_pages

# Instancia global que será inicializada desde main.py
rag_engine = None