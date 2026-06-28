import os
from pathlib import Path
from parse_md_blocks import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    if not os.path.exists(from_path):
        raise Exception(f"{from_path} path does not exist")

    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content)

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    from_path = Path(dir_path_content)
    dest_dir = Path(dest_dir_path)

    md_files = list(from_path.glob('**/*.md'))

    for md_file in md_files:
        relative_path = md_file.relative_to(from_path)
        dest_path = dest_dir / relative_path.with_suffix(".html")

        generate_page(md_file, template_path, dest_path)
        