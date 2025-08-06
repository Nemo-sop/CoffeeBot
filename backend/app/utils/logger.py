from loguru import logger
import sys
from pathlib import Path

Path("logs").mkdir(exist_ok=True)

logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/debug.log", rotation="1 MB", level="DEBUG", retention="10 days", enqueue=True)

logger.info("Logger initialized")