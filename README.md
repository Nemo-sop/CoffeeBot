# ☕ CoffeeBot — Chat Conversacional sobre Café

CoffeeBot es un chatbot inteligente diseñado para responder exclusivamente preguntas sobre café. Usa una arquitectura basada en RAG (Retrieval Augmented Generation) para responder de forma precisa, validando idioma y temática antes de mostrar la respuesta final.

Este proyecto fue desarrollado como take-home assignment y simula un producto listo para producción, con backend (FastAPI), frontend (Streamlit), tests, contenedores Docker, y CI/CD para despliegue en la nube.

---

## 🧠 Razonamiento detrás del diseño

CoffeeBot fue pensado bajo principios de **modularidad**, **validación robusta**, y **desacoplamiento entre componentes**. Algunos puntos clave del enfoque:

- **Backend en FastAPI**: sirve como API para manejar preguntas, ejecutar RAG, llamar al modelo de lenguaje y validar las respuestas.
- **RAG local con FAISS**: para evitar dependencias externas, se realiza la indexación y recuperación en memoria a partir de un PDF (`coffee-recipes.pdf`).
- **Validaciones avanzadas**:
  - **Idioma**: solo se permite español. Se detecta el input y también el output del LLM para evitar respuestas en inglés u otros idiomas.
  - **Temática**: si la respuesta no tiene suficiente similitud con vectores relacionados al café, se descarta y se regenera automáticamente.
- **LLM wrapper**: el diseño está desacoplado para permitir fácilmente cambiar el modelo base (Gemini, Mistral, TinyLlama, etc.).
- **Frontend en Streamlit**: visual profesional con burbujas de conversación, scroll independiente y UX clara (feedback cuando se regenera una respuesta).
- **CI/CD**: preparado para Docker + DockerHub + Render o Kubernetes.
- **Conversación con contexto**: se mantiene el historial de usuario y bot para mejorar la comprensión de cada mensaje.

---

## ▶️ Cómo correr la app localmente

Requisitos:

- Docker instalado
- Python 3.10+ (solo si querés correr sin Docker)

### 🐳 Opción A: usando Docker 

```bash
# Cloná el repo
git clone https://github.com/Nemo-sop/CoffeeBot.git
cd CoffeeBot

# Build y correr backend y frontend
docker compose up --build
```
Esto expondrá:
http://localhost:8000 → API de FastAPI
http://localhost:8501 → Interfaz en Streamlit

### 🧪 Opción B: correr manualmente 

1. Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
2. Frontend
En otro terminal:

```bash
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```
---

## ⚙️ Variables de entorno
Crear archivo .env con:

```bash
GEMINI_API_KEY=tu_clave_de_gemini
LOG_LEVEL=INFO
APP_ENV=development
```
---

## 🧠 Consideraciones
El PDF se carga e indexa al iniciar la API. Esto puede tomar unos segundos la primera vez.
La validación de respuestas es estricta: si el bot responde en inglés o con baja relevancia, se regenera automáticamente la respuesta hasta un maximo de 3 veces.
No se usa una base vectorial externa: FAISS funciona en memoria para facilitar despliegue rápido.
No se permite hablar de temas no relacionados al café ni en otro idioma que no sea el español. El bot lo expresará explícitamente.

---
## 🚧 TODOs / Mejoras futuras
 - Agregar soporte para respuestas enriquecidas (imágenes, recetas, enlaces)
 - Persistir conversaciones y métricas con una base de datos
 - Entrenar un modelo embebido especializado en café como endgame
 - Tener un modelo en local como fallback cuando el free tier de gemini esta muy lento. ej: Mistral-7B
 - Deploy automatizado con GitHub Actions + DockerHub
 - Más validaciones semánticas sobre respuestas (al menos ahcer un analisis mas profundo para settear un mejor threshold de similitud)
 - UI más responsiva para mobile (ajustes de CSS) y en general mas atractiva para mejorar la UX
 - Panel administrativo para auditar conversaciones y rendimiento
 - Autenticación para personalizar respuestas por usuario y un mejor manejod e sesiones
 
 ---
 
 ## 💡 Modal como solución técnica viable (no implementada)
 
 Uno de los requerimientos del proyecto es el uso de FastAPI como framework para construir el backend. La aplicación cumple con este requisito desde su diseño inicial: el backend completo está construido con FastAPI, incluyendo sus rutas, validaciones, esquema OpenAPI/Swagger y arquitectura modular.

Sin embargo, debido a las restricciones de memoria de servicios como Render Free Tier (512 MiB), el backend no puede ser desplegado allí de forma confiable, ya que realiza:

- Indexación en memoria de un PDF con FAISS
- Generación de embeddings con Gemini
- Procesamiento intensivo al iniciar


Durante el desarrollo del proyecto, se consideró el uso de Modal como una solución alternativa para desplegar el backend. Modal es una plataforma serverless que permite exponer aplicaciones web como funciones escalables con mayor capacidad de cómputo que Render Free Tier (512 MiB de RAM).

Sin embargo, no se implementó esta opción por respeto a las pautas del assignment, que indicaban explícitamente el uso de FastAPI. Aunque Modal permite montar apps FastAPI como aplicaciones ASGI, hacerlo requiere modificar el punto de entrada (uvicorn → modal.asgi_app()), lo que puede ser interpretado como un desvío del requisito original.

Aclaración importante:

- Toda la lógica del backend está desarrollada en FastAPI
- La arquitectura es completamente compatible con Modal

La opción de usar Modal fue analizada y documentada como una mejora factible para superar la limitación de memoria sin romper el diseño base
 
 ---
 
## ⏳ Consideración sobre el tiempo de desarrollo
Se hizo un esfuerzo consciente por respetar la estimación de tiempo original del assignment, que indicaba que la tarea podía completarse en unas pocas horas.

Para cumplir con esta expectativa:

- Se priorizó una arquitectura funcional y escalable sin sobre-ingeniería
- Se documentaron decisiones técnicas sin extender el alcance con funcionalidades no requeridas
- Se dejó explícito en la sección de TODOs qué mejoras fueron identificadas pero no implementadas

El objetivo fue entregar una solución madura, pero alineada con los límites temporales propuestos, tal como se esperaría en un entorno profesional.
