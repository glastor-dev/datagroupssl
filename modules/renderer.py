from typing import Dict, List, Optional
import logging

class MarkdownRenderer:
    """Renderiza componentes a Markdown con formato profesional"""

    def render_header(self, title: str, subtitle: str = "", emoji: str = "") -> str:
        """Genera el encabezado del README"""
        return f"# {title} {emoji}\n\n{subtitle}\n\n---\n"

    def render_hero(self, image_url: str, link: str, align: str = "right",
                   width: int = 300, caption: str = "") -> str:
        """Genera una imagen hero con alineación"""
        return (
            f'<div align="{align}">\n'
            f'  <a href="{link}">\n'
            f'    <img src="{image_url}" width="{width}" alt="{caption}"/>\n'
            f'  </a>\n'
            f'  <p align="center"><em>{caption}</em></p>\n'
            f'</div>\n\n'
        )

    def render_quote(self, text: str, author: str, icon: str = "💡") -> str:
        """Renderiza una cita con formato"""
        return f"> {icon} **{text}**  \n> — *{author}*\n\n"

    def render_projects(self, title: str, repos: List[Dict],
                       show_tech_tags: bool = True, show_stars: bool = True) -> str:
        """Genera una tabla de proyectos con badges"""
        if not repos:
            return f"## {title}\n\nNo hay proyectos para mostrar\n\n"

        # Cabecera de la tabla
        table = (
            f"## {title}\n\n"
            "| Proyecto | Descripción | Tecnologías |\n"
            "|----------|-------------|-------------|\n"
        )

        for repo in repos:
            # Validación básica de campos requeridos
            name = repo.get('name', 'Sin nombre')
            url = repo.get('html_url', '#')
            description = repo.get('description', '')
            description = (description[:100] + '...') if len(description) > 100 else description

            # Obtener lenguajes principales (top 3)
            languages = ", ".join(list(repo.get("languages", {}).keys())[:3])

            # Construir badges de tecnologías
            tech_badges = f"<sub>{languages}</sub>" if show_tech_tags and languages else ""

            # Construir badges de estrellas
            stars_badge = f"⭐ {repo.get('stargazers_count', 0)}" if show_stars and repo.get('stargazers_count', 0) > 0 else ""

            table += (
                f"| [{name}]({url}) "
                f"| {description} "
                f"| {tech_badges} {stars_badge} |\n"
            )

        return table + "\n"

    def render_contact(self, title: str, links: List[Dict]) -> str:
        """Genera la sección de contacto con iconos"""
        contact_md = f"## {title}\n\n<div align=\"center\">\n"

        for link in links:
            url = link.get("url", "#")
            icon = link.get("icon", "")
            platform = link.get("platform", "")
            contact_md += (
                f'<a href="{url}" target="_blank">'
                f'<img src="{icon}" alt="{platform}" '
                f'width="40" height="40" style="margin: 0 10px;"/></a>\n'
            )

        contact_md += "</div>\n\n"
        return contact_md
