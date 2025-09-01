import os

from jinja2 import Environment, FileSystemLoader


def jinja_env(template_dir: str) -> Environment:
    return Environment(
        loader=FileSystemLoader(template_dir),
        variable_start_string="<<",
        variable_end_string=">>",
        block_start_string="<%",  # for control structures
        block_end_string="%>",
        comment_start_string="<#",
        comment_end_string="#>",
    )


def render_file(template_path: str, data: dict) -> str:
    # Extract directory and file name
    template_dir = os.path.dirname(template_path)
    template_file = os.path.basename(template_path)

    # Create Jinja environment
    # env = Environment(loader=FileSystemLoader(template_dir))
    env = jinja_env(template_dir)
    template = env.get_template(template_file)

    # Render the template with data
    return template.render(**data)


def remove_lines_with_string(file_path: str, target: str) -> None:
    """
    Removes lines from a file that contain the given target string.

    Args:
        file_path (str): Path to the file.
        target (str): Substring to search for in lines to remove.
    """
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    filtered_lines = [line for line in lines if target not in line]

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(filtered_lines)


html_template_path = "./templates/extension_builder_stub/index.html"
rendered_html = render_file(
    html_template_path,
    {
        "title": "My Page XXXXXXX",
        "content": "This is the content of my page.",
        "items": ["Item 1", "Item 2", "Item 3"],
    },
)

# Overwrite the original file with rendered content
with open(html_template_path, "w", encoding="utf-8") as f:
    f.write(rendered_html)


remove_line_marker = "{remove_line_marker}}"
py_template_path = "./models.py"
rendered_html = render_file(
    py_template_path,
    {
        "table": {
            "name": "Campaign",
            "fields": [
                {"name": "description", "type": "str"},
                {"name": "amount", "type": "int", "optional": True},
            ],
        },
        "cancel_comment": remove_line_marker,
    },
)

# Overwrite the original file with rendered content
with open("./models2.py", "w", encoding="utf-8") as f:
    f.write(rendered_html)

remove_lines_with_string("./models2.py", remove_line_marker)
