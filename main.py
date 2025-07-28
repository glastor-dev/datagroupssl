import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from modules.github_api import GitHubAPI
from modules.generator import READMEGenerator
from modules.renderer import MarkdownRenderer
from utils.file_utils import load_config, save_readme
from utils.logging_utils import configure_logging

def main():
    configure_logging()

    try:
        # Cargar configuración
        config = load_config(Path("config/template.json"))

        # Inicializar componentes
        github_api = GitHubAPI(config["github_user"])
        renderer = MarkdownRenderer()
        generator = READMEGenerator(github_api, renderer)

        # Generar README
        readme_content = generator.generate(config)

        # Guardar archivo
        save_readme(Path("README.md"), readme_content)

        logging.info("README generado exitosamente")
    except Exception as e:
        logging.error(f"Error al generar README: {str(e)}")
        raise

if __name__ == "__main__":
    main()
