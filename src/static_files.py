import os
import shutil


def copy_static_to_public(source_dir, dest_dir):
    """
    Recursively copy all contents from source directory to destination directory.
    First clears the destination directory to ensure a clean copy.
    
    Args:
        source_dir: Path to the source directory
        dest_dir: Path to the destination directory
    """
    print(f"Copying static files from {source_dir} to {dest_dir}")
    
    # Delete destination directory if it exists
    if os.path.exists(dest_dir):
        print(f"Clearing destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    # Create the destination directory
    print(f"Creating destination directory: {dest_dir}")
    os.mkdir(dest_dir)
    
    # Recursively copy all contents
    _copy_directory_contents(source_dir, dest_dir)
    
    print("Static file copy completed!")


def _copy_directory_contents(source_dir, dest_dir):
    """
    Recursively copy directory contents.
    
    Args:
        source_dir: Path to the source directory
        dest_dir: Path to the destination directory
    """
    if not os.path.exists(source_dir):
        print(f"Warning: Source directory {source_dir} does not exist")
        return
    
    # List all items in the source directory
    items = os.listdir(source_dir)
    
    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_path):
            # Copy file
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            # Create directory and recursively copy its contents
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            _copy_directory_contents(source_path, dest_path)
