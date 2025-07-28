from typing import Dict, List, Optional
import requests
from requests.exceptions import RequestException
import logging
from datetime import datetime
from cachetools import cached, TTLCache

class GitHubAPI:
    """Cliente para la API de GitHub con caché y manejo de errores"""

    def __init__(self, github_user: str):
        self.github_user = github_user
        self.base_url = f"https://api.github.com/users/{github_user}"
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "README-Generator/1.0"
        })
        self.cache = TTLCache(maxsize=100, ttl=3600)  # 1 hora de caché

    @cached(cache)
    def get_user_info(self) -> Dict:
        """Obtiene información básica del usuario"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logging.error(f"Error al obtener info de usuario: {str(e)}")
            return {}

    @cached(cache)
    def get_repos(self, sort: str = "updated") -> List[Dict]:
        """Obtiene repositorios públicos ordenados"""
        try:
            url = f"{self.base_url}/repos?sort={sort}&direction=desc"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logging.error(f"Error al obtener repositorios: {str(e)}")
            return []

    def get_filtered_repos(self, filter_by: str) -> List[Dict]:
        """Filtra repositorios por tecnología"""
        repos = self.get_repos()
        return [repo for repo in repos if filter_by.lower() in repo["name"].lower()]

    def get_repo_languages(self, repo_name: str) -> Dict:
        """Obtiene lenguajes de un repositorio específico"""
        try:
            url = f"https://api.github.com/repos/{self.github_user}/{repo_name}/languages"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logging.error(f"Error al obtener lenguajes: {str(e)}")
            return {}
