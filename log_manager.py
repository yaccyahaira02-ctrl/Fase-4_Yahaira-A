# ARCHIVO 2: Registro de eventos y errores.
# modelos.py y main.py usan: from log_manager import logger

# MÓDULO DE GESTIÓN DE REGISTROS (LOGS)
# ===========================================

import logging # Importa la librería nativa para generar registros y auditorías
import os      # Importa la librería para interactuar con directorios del sistema operativo

def configurar_logger():
    """Configura el archivo de registro para guardar eventos y errores sin usar bases de datos."""
    # Crea la carpeta 'logs' automáticamente si no existe en el proyecto
    os.makedirs(os.path.join(os.path.dirname(__file__), "logs"), exist_ok=True)
    
    # Obtiene o crea un canal de registro con un nombre específico
    logger = logging.getLogger("SoftwareFJLogger")
    logger.setLevel(logging.INFO) # Define el nivel mínimo para registrar (INFO, WARNING, ERROR)
    
    # Evita duplicar manejadores si la función se llama varias veces
    if not logger.handlers:
        # Configura el archivo de texto plano donde se guardarán los logs
        handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), "logs", "sistema_fj.log"), encoding="utf-8")
        # Define el formato visual que tendrá cada línea de registro (Fecha/Hora - Nivel - Mensaje)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

# Instancia global del logger para ser usada en todo el sistema
logger = configurar_logger()

# ==========================================
