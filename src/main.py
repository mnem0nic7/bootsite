import os
from textnode import TextNode, TextType
from static_files import copy_static_to_public


def main():
    # Get the project root directory (parent of src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    # Define source and destination paths
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    content_dir = os.path.join(project_root, "content")
    template_html = os.path.join(project_root, "template.html")

    # Clean public directory if it exists
    if os.path.exists(public_dir):
        import shutil
        print(f"Deleting existing public directory: {public_dir}")
        shutil.rmtree(public_dir)

    # Copy static files to public directory
    copy_static_to_public(static_dir, public_dir)

    # Generate all pages recursively
    from pagegen import generate_pages_recursive
    generate_pages_recursive(content_dir, template_html, public_dir)

    print("Static site generation completed!")

if __name__ == "__main__":
    main()
