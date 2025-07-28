from pathlib import Path
import json
from typing import Dict, Any
import logging

def load_config(config_path: Path) -> Dict[str, Any]:
    """Carga el archivo de configuración JSON"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error al cargar configuración: {str(e)}")
        raise

def save_readme(output_path: Path, content: str) -> None:
    """Guarda el README generado"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        logging.error(f"Error al guardar README: {str(e)}")
        raise
