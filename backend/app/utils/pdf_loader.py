import fitz
from .logger import logger
from typing import List

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extrae texto concatenado de todo el PDF (para compatibilidad)"""
    logger.info(f"Cargando PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    text = ""
    for page_num, page in enumerate(doc):
        page_text = page.get_text()
        logger.debug(f"Texto extraído de página {page_num + 1}")
        text += page_text + "\n"
    logger.info(f"PDF cargado. Total de páginas: {len(doc)}")
    return text

def extract_pages_from_pdf(pdf_path: str) -> List[str]:
    """Extrae texto página por página, devolviendo una lista donde cada elemento es una página"""
    logger.info(f"Cargando PDF por páginas: {pdf_path}")
    doc = fitz.open(pdf_path)
    pages = []
    
    for page_num, page in enumerate(doc):
        page_text = page.get_text().strip()
        if page_text:  # Solo agregar páginas que no estén vacías
            pages.append(page_text)
            logger.debug(f"Página {page_num + 1} extraída: {len(page_text)} caracteres")
        else:
            logger.debug(f"Página {page_num + 1} está vacía, omitiendo")
    
    logger.info(f"📄 PDF cargado: {len(pages)} páginas con contenido")
    return pages