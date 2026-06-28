from copy_static import copy_origin_to_destination
from generate_page import generate_page, generate_pages_recursive


def main():
    copy_origin_to_destination("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")

main()