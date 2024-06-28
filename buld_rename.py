import os

def bulk_rename(root_dir, old_pattern, new_pattern):
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if old_pattern in filename:
                old_path = os.path.join(root, filename)
                new_filename = filename.replace(old_pattern, new_pattern)
                new_path = os.path.join(root, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")

# Example usage
root_directory = "/path/to/your/folder"
old_pattern = "old_text"
new_pattern = "new_text"

bulk_rename(root_directory, old_pattern, new_pattern)