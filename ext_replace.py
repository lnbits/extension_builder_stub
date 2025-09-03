import json
import os
import re

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


def camel_to_snake(name: str) -> str:
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def field_to_py(field: dict) -> str:
    field_name = camel_to_snake(field["name"])
    field_type = field["type"]
    if field_type == "json":
        field_type = "dict"
    elif field_type in ["wallet", "currency"]:
        field_type = "str"
    if field["optional"]:
        field_type += " | None"
    return f"{field_name}: {field_type}"


def field_to_db(field: dict) -> str:
    field_name = camel_to_snake(field["name"])
    field_type = field["type"]
    if field_type == "str":
        db_type = "TEXT"
    elif field_type == "int":
        db_type = "INT"
    elif field_type == "float":
        db_type = "REAL"
    elif field_type == "bool":
        db_type = "BOOLEAN"
    elif field_type == "datetime":
        db_type = "TIMESTAMP"
    else:
        db_type = "TEXT"

    db_field = f"{field_name} {db_type}"
    if not field["optional"]:
        db_field += " NOT NULL"
    if field_type == "json":
        db_field += " DEFAULT '{empty_dict}'"
    return db_field


def field_to_ui_table_column(field: dict) -> str:
    column = {
        "name": field["name"],
        "align": "left",
        "label": field["label"],
        "field": field["name"],
        "sortable": field["sortable"],
    }

    return json.dumps(column)



remove_line_marker = "{remove_line_marker}}"
py_template_path = "./models.py"

data = {
    "owner_table": {
        "name": "Campaign",
        "fields": [
            {
                "name": "id",
                "type": "str",
                "label": "ID",
                "hint": "Unique identifier",
                "optional": False,
                "editable": False,
                "searchable": False,
                "sortable": True,
            },
            {
                "name": "name",
                "type": "str",
                "label": "Name",
                "hint": "Name of the campaign",
                "optional": False,
                "editable": True,
                "searchable": True,
                "sortable": True,
            },
            {
                "name": "description",
                "type": "str",
                "label": "Description",
                "hint": "Description of the campaign",
                "optional": False,
                "editable": True,
                "searchable": True,
                "sortable": True,
            },
            {
                "name": "email",
                "label": "Email",
                "hint": "Contact email",
                "type": "str",
                "optional": True,
                "editable": True,
                "searchable": True,
                "sortable": True,
            },
            {
                "name": "wallet_id",
                "label": "Wallet ID",
                "hint": "Unique identifier for the wallet",
                "type": "wallet",
                "optional": False,
                "editable": True,
                "searchable": False,
                "sortable": False,
            },
            {
                "name": "extra",
                "type": "json",
                "optional": False,
                "editable": False,
                "searchable": False,
                "sortable": False,
            },
        ],
        "public_fields": ["name", "description"],
    },
    "client_table": {
        "name": "Donations",
        "fields": [
            {
                "name": "id",
                "type": "str",
                "optional": False,
                "editable": False,
                "searchable": False,
            },
            {
                "name": "amount_sats",
                "type": "int",
                "optional": False,
                "editable": False,
                "searchable": True,
            },
            {
                "name": "description",
                "type": "str",
                "optional": True,
                "editable": False,
                "searchable": False,
            },
        ],
    },
}

parsed_data = {
    "owner_table": {
        "name": data["owner_table"]["name"],
        "editable_fields": [
            field_to_py(field)
            for field in data["owner_table"]["fields"]
            if field["editable"]
        ],
        "search_fields": [
            camel_to_snake(field["name"])
            for field in data["owner_table"]["fields"]
            if field["searchable"]
        ],
        "public_fields": [
            field_to_py(field)
            for field in data["owner_table"]["fields"]
            if field["name"] in data["owner_table"]["public_fields"]
        ],
        "ui_table_columns": [
            field_to_ui_table_column(field)
            for field in data["owner_table"]["fields"]
            if field["sortable"]
        ],
        "db_fields": [field_to_db(field) for field in data["owner_table"]["fields"]],
        "all_fields": [field_to_py(field) for field in data["owner_table"]["fields"]],
    },
    "client_table": {
        "name": data["client_table"]["name"],
        "editable_fields": [
            field_to_py(field)
            for field in data["client_table"]["fields"]
            if field["editable"]
        ],
        "all_fields": [field_to_py(field) for field in data["client_table"]["fields"]],
    },
    "cancel_comment": remove_line_marker,
}


py_files = [
    "__init__.py",
    "models.py",
    "migrations.py",
    "views_api.py",
    "crud.py",
    "views.py",
    "tasks.py",
    "services.py",
]

# Overwrite the original file with rendered content


def test():
    for py_file in py_files:
        template_path = f"./{py_file}"
        rederer = render_file(template_path, parsed_data)
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(rederer)

        remove_lines_with_string(template_path, remove_line_marker)


# test()

template_path = "./static/js/index.js"
rederer = render_file(template_path, parsed_data)
with open(template_path, "w", encoding="utf-8") as f:
    f.write(rederer)

remove_lines_with_string(template_path, remove_line_marker)
