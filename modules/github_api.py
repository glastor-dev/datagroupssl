from typing import Dict, List, Optional, Any
import requests
from requests.exceptions import RequestException
import logging
from cachetools import TTLCache, cachedmethod
from operator import attrgetter

class GitHubAPI:
    """Cliente para la API de GitHub con caché, manejo de errores y autenticación opcional."""

    def __init__(self, github_user: str, token: Optional[str] = None, cache_maxsize: int = 100, cache_ttl: int = 3600):
        self.github_user = github_user
        self.base_url = f"https://api.github.com/users/{github_user}"
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "README-Generator/1.0"
        })
        if token:
            self.session.headers.update({"Authorization": f"token {token}"})
        self.cache = TTLCache(maxsize=cache_maxsize, ttl=cache_ttl)  # Caché configurable

    @cachedmethod(attrgetter('cache'))
    def get_user_info(self) -> Dict[str, Any]:
        """Obtiene información básica del usuario."""
        try:
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logging.error(f"Error al obtener info de usuario '{self.github_user}': {str(e)}")
            return {}

    @cachedmethod(attrgetter('cache'))
    def get_repos(self, sort: str = "updated", per_page: int = 100, max_pages: int = 5) -> List[Dict[str, Any]]:
        """Obtiene todos los repositorios públicos ordenados, manejando paginación."""
        repos = []
        page = 1
        try:
            while page <= max_pages:
                url = f"{self.base_url}/repos?sort={sort}&direction=desc&per_page={per_page}&page={page}"
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                data = response.json()
                if not data:
                    break
                repos.extend(data)
                if len(data) < per_page:
                    break
                page += 1
            return repos
        except RequestException as e:
            logging.error(f"Error al obtener repositorios de '{self.github_user}': {str(e)}")
            return []

    def get_filtered_repos(self, filter_by: str, field: str = "name") -> List[Dict[str, Any]]:
        """
        Filtra repositorios por un campo específico (por defecto, nombre).
        :param filter_by: Texto a buscar.
        :param field: Campo del repo a filtrar (name, language, etc).
        """
        repos = self.get_repos()
        return [repo for repo in repos if filter_by.lower() in str(repo.get(field, "")).lower()]

    def get_repo_languages(self, repo_name: str) -> Dict[str, int]:
        """Obtiene lenguajes de un repositorio específico."""
        try:
            url = f"https://api.github.com/repos/{self.github_user}/{repo_name}/languages"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logging.error(f"Error al obtener lenguajes del repo '{repo_name}': {str(e)}")
            return {}
