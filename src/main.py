import os
import sys
from textnode import TextNode, TextType
from static_files import copy_static_to_public


def main():
    # Get basepath from command line argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    # Get the project root directory (parent of src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    # Define source and destination paths
    static_dir = os.path.join(project_root, "static")
    docs_dir = os.path.join(project_root, "docs")  # Changed from public to docs
    content_dir = os.path.join(project_root, "content")
    template_html = os.path.join(project_root, "template.html")

    # Clean docs directory if it exists
    if os.path.exists(docs_dir):
        import shutil
        print(f"Deleting existing docs directory: {docs_dir}")
        shutil.rmtree(docs_dir)

    # Copy static files to docs directory
    copy_static_to_public(static_dir, docs_dir)

    # Generate all pages recursively
    from pagegen import generate_pages_recursive
    generate_pages_recursive(content_dir, template_html, docs_dir, basepath)

    print("Static site generation completed!")

if __name__ == "__main__":
    main()
