"""
Configuración de logging para Treqe
"""

import logging
import sys
from pathlib import Path
from .config import settings

def setup_logging():
    """
    Configurar logging estructurado para la aplicación
    """
    # Crear directorio de logs si no existe
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configurar formato
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Configurar nivel de logging
    log_level = getattr(logging, settings.LOG_LEVEL.upper())
    
    # Configurar handlers
    handlers = []
    
    # Handler para archivo
    file_handler = logging.FileHandler(settings.LOG_FILE)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    handlers.append(file_handler)
    
    # Handler para consola (solo en desarrollo)
    if settings.ENVIRONMENT in ["development", "staging"]:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(logging.Formatter(log_format, date_format))
        handlers.append(console_handler)
    
    # Configurar logging root
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )
    
    # Configurar loggers específicos
    loggers_to_configure = [
        "uvicorn",
        "fastapi",
        "sqlalchemy",
        "celery",
        "treqe"
    ]
    
    for logger_name in loggers_to_configure:
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
        logger.handlers = []  # Remover handlers existentes
        for handler in handlers:
            logger.addHandler(handler)
        logger.propagate = False
    
    # Logger principal de Treqe
    treqe_logger = logging.getLogger("treqe")
    treqe_logger.info(f"Logging configured for {settings.ENVIRONMENT} environment")
    treqe_logger.info(f"Log level: {settings.LOG_LEVEL}")
    treqe_logger.info(f"Log file: {settings.LOG_FILE}")

def get_logger(name: str) -> logging.Logger:
    """
    Obtener logger con prefijo 'treqe'
    """
    logger_name = f"treqe.{name}"
    return logging.getLogger(logger_name)

# Logging estructurado para JSON (opcional para producción)
class StructuredLogger:
    """Logger estructurado para producción"""
    
    def __init__(self, name: str):
        self.logger = get_logger(name)
    
    def info(self, message: str, **kwargs):
        """Log info con metadata"""
        if kwargs:
            self.logger.info(f"{message} | {kwargs}")
        else:
            self.logger.info(message)
    
    def warning(self, message: str, **kwargs):
        """Log warning con metadata"""
        if kwargs:
            self.logger.warning(f"{message} | {kwargs}")
        else:
            self.logger.warning(message)
    
    def error(self, message: str, error: Exception = None, **kwargs):
        """Log error con metadata"""
        if error:
            kwargs["error"] = str(error)
            kwargs["error_type"] = type(error).__name__
        
        if kwargs:
            self.logger.error(f"{message} | {kwargs}")
        else:
            self.logger.error(message)
    
    def debug(self, message: str, **kwargs):
        """Log debug con metadata"""
        if kwargs:
            self.logger.debug(f"{message} | {kwargs}")
        else:
            self.logger.debug(message)

# Logger global para uso rápido
logger = StructuredLogger("app")