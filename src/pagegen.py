def extract_title(markdown):
    """
    Extract the first H1 header from the markdown string and return its text.
    Raises ValueError if no H1 header is found.
    """
    for line in markdown.splitlines():
        if line.strip().startswith('# '):
            return line.strip()[2:].strip()
    raise Exception("No H1 header found in markdown")


def generate_page(from_path, template_path, dest_path):
    import os
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Read markdown
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown = f.read()
    # Read template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    # Convert markdown to HTML
    from markdown_to_html import markdown_to_html_node
    html = markdown_to_html_node(markdown).to_html()
    # Extract title
    title = extract_title(markdown)
    # Replace placeholders
    page = template.replace('{{ Title }}', title).replace('{{ Content }}', html)
    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    # Write output
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    import os
    
    # Get all entries in the content directory
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(entry_path):
            # If it's a markdown file, generate HTML page
            if entry.endswith('.md'):
                # Calculate the destination HTML file path
                html_filename = entry.replace('.md', '.html')
                dest_file_path = os.path.join(dest_dir_path, html_filename)
                
                # Generate the page
                generate_page(entry_path, template_path, dest_file_path)
        else:
            # If it's a directory, recurse into it
            # Create corresponding directory in destination
            dest_subdir = os.path.join(dest_dir_path, entry)
            os.makedirs(dest_subdir, exist_ok=True)
            
            # Recursively process the subdirectory
            generate_pages_recursive(entry_path, template_path, dest_subdir)
