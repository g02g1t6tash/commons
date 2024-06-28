import os

def get_files_with_extension(directory, extension):
    """
    Get a list of files with a specific extension from the given directory.

    Args:
    directory (str): The path to the directory to search.
    extension (str): The file extension to look for (e.g., '.txt', '.py').

    Returns:
    list: A list of file names with the specified extension.
    """
    # Ensure the extension starts with a dot
    if not extension.startswith('.'):
        extension = '.' + extension

    # List to store matching files
    matching_files = []

    # Walk through the directory
    for root, _, files in os.walk(directory):
        for file in files:
            # Check if the file has the specified extension
            if file.endswith(extension):
                # Add the full path of the file to the list
                matching_files.append(os.path.join(root, file))

    return matching_files

# Example usage
if __name__ == "__main__":
    directory_path = "/path/to/your/directory"
    file_extension = ".txt"
    
    files = get_files_with_extension(directory_path, file_extension)
    
    print(f"Files with extension '{file_extension}' in '{directory_path}':")
    for file in files:
        print(file)