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
            return "## Proyectos\n\nNo hay proyectos para mostrar\n\n"

        # Cabecera de la tabla
        table = (
            f"## {title}\n\n"
            "| Proyecto | Descripción | Tecnologías |\n"
            "|----------|-------------|-------------|\n"
        )

        for repo in repos:
            # Obtener lenguajes principales (top 3)
            languages = ", ".join(repo.get("languages", {}).keys()[:3])

            # Construir badges de tecnologías
            tech_badges = ""
            if show_tech_tags and languages:
                tech_badges = f"<sub>{languages}</sub>"

            # Construir badges de estrellas
            stars_badge = ""
            if show_stars and repo.get("stargazers_count", 0) > 0:
                stars_badge = f"⭐ {repo['stargazers_count']}"

            table += (
                f"| [{repo['name']}]({repo['html_url']}) "
                f"| {repo.get('description', '')[:100]}... "
                f"| {tech_badges} {stars_badge} |\n"
            )

        return table + "\n"

    def render_contact(self, title: str, links: List[Dict]) -> str:
        """Genera la sección de contacto con iconos"""
        contact_md = f"## {title}\n\n<div align=\"center\">\n"

        for link in links:
            contact_md += (
                f'<a href="{link["url"]}" target="_blank">'
                f'<img src="{link["icon"]}" alt="{link["platform"]}" '
                f'width="40" height="40" style="margin: 0 10px;"/></a>\n'
            )

        contact_md += "</div>\n\n"
        return contact_md
