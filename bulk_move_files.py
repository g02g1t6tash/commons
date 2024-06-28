import os
import shutil

def move_files(source_dir, destination_dir):
    # Walk through the source directory
    for root, dirs, files in os.walk(source_dir):
        # Create the corresponding directory structure in the destination
        relative_path = os.path.relpath(root, source_dir)
        dest_path = os.path.join(destination_dir, relative_path)
        os.makedirs(dest_path, exist_ok=True)
        
        # Move each file to the destination
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_path, file)
            shutil.move(src_file, dst_file)
            print(f"Moved: {src_file} -> {dst_file}")

# Example usage
source_directory = "/path/to/source/folder"
destination_directory = "/path/to/destination/folder"

move_files(source_directory, destination_directory)