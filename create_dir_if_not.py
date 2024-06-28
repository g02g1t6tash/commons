import os

def create_directory(path):
    """
    Create a new directory if it doesn't exist.
    
    Args:
    path (str): The path of the directory to be created.
    
    Returns:
    bool: True if the directory was created, False if it already existed.
    """
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory '{path}' created successfully.")
        return True
    except OSError as error:
        print(f"Error creating directory '{path}': {error}")
        return False

# Example usage
if __name__ == "__main__":
    new_dir_path = "path/to/new/directory"
    create_directory(new_dir_path)