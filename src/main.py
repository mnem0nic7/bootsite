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
    
    # Copy static files to public directory
    copy_static_to_public(static_dir, public_dir)
    
    print("Static site generation completed!")

if __name__ == "__main__":
    main()
