from typing import Dict, List
from datetime import datetime
import logging
from modules.github_api import GitHubAPI
from modules.renderer import MarkdownRenderer

class READMEGenerator:
    """Genera README.md dinámico basado en templates"""

    def __init__(self, github_api: GitHubAPI, renderer: MarkdownRenderer):
        self.github = github_api
        self.renderer = renderer

    def generate(self, config: Dict) -> str:
        """Genera el contenido completo del README"""
        sections = []
        context = self._build_context(config)

        for section in config["sections"]:
            try:
                content = self._render_section(section, context)
                if content:
                    sections.append(content)
            except Exception as e:
                logging.warning(f"Error renderizando sección {section.get('type')}: {str(e)}")
                continue

        return "\n".join(sections)

    def _build_context(self, config: Dict) -> Dict:
        """Construye el contexto con datos actualizados"""
        user_info = self.github.get_user_info()
        repos = self.github.get_repos()

        return {
            "user": user_info,
            "repos": repos,
            "categories": config.get("categories", []),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "year": datetime.now().year
        }

    def _render_section(self, section: Dict, context: Dict) -> str:
        """Renderiza una sección individual"""
        section_type = section["type"]
        data = section["data"]

        if section_type == "header":
            return self.renderer.render_header(
                title=data["title"],
                subtitle=data.get("subtitle", ""),
                emoji=data.get("emoji", "")
            )
        elif section_type == "hero":
            return self.renderer.render_hero(
                image_url=data["image"],
                link=data["link"],
                align=data.get("align", "right"),
                width=data.get("width", 300),
                caption=data.get("caption", "")
            )
        elif section_type == "quote":
            return self.renderer.render_quote(
                text=data["text"],
                author=data["author"],
                icon=data.get("icon", "💡")
            )
        elif section_type == "projects":
            return self._render_projects_section(data, context)
        elif section_type == "contact":
            return self.renderer.render_contact(
                title=data["title"],
                links=data["links"]
            )

        return ""

    def _render_projects_section(self, data: Dict, context: Dict) -> str:
        """Renderiza la sección de proyectos"""
        count = min(data["count"], 10)  # Limitar a 10 proyectos máximo
        filtered_repos = []

        for category in context["categories"]:
            filtered_repos.extend(
                self.github.get_filtered_repos(category["tag"])[:count]
            )

        # Ordenar por estrellas y actualización
        filtered_repos.sort(
            key=lambda r: (r.get("stargazers_count", 0), r.get("pushed_at", "")),
            reverse=True
        )

        return self.renderer.render_projects(
            title=data["title"],
            repos=filtered_repos[:count],
            show_tech_tags=data.get("show_tech_tags", False),
            show_stars=data.get("show_stars", True)
        )
