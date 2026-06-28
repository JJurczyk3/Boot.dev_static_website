from copy_static import copy_origin_to_destination
from generate_page import generate_page, generate_pages_recursive
import sys


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_origin_to_destination("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()