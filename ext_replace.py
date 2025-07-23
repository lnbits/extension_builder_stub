import os

from jinja2 import Environment, FileSystemLoader


def render_html(template_path: str, data: dict) -> str:
    # Extract directory and file name
    template_dir = os.path.dirname(template_path)
    template_file = os.path.basename(template_path)

    # Create Jinja environment
    # env = Environment(loader=FileSystemLoader(template_dir))
    env = Environment(
        loader=FileSystemLoader(template_dir),
        variable_start_string="[[",
        variable_end_string="]]",
        block_start_string="[%",  # for control structures
        block_end_string="%]",
        comment_start_string="[#",
        comment_end_string="#]",
    )
    template = env.get_template(template_file)

    # Render the template with data
    return template.render(**data)


template_path = "./templates/extension_builder_stub/index.html"
rendered_html = render_html(
    template_path,
    {
        "title": "My Page XXXXXXX",
        "content": "This is the content of my page.",
        "items": ["Item 1", "Item 2", "Item 3"],
    },
)

# Overwrite the original file with rendered content
with open(template_path, "w", encoding="utf-8") as f:
    f.write(rendered_html)
