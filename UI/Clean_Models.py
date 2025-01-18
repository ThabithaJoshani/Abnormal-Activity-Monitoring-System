import os
import shutil


def delete_files_in_directory(directory):
    """
    Delete all files and folders inside the specified directory.

    :param directory: Path to the directory whose contents need to be deleted.
    """
    if os.path.exists(directory):
        for file_or_folder in os.listdir(directory):
            file_or_folder_path = os.path.join(directory, file_or_folder)
            try:
                if os.path.isfile(file_or_folder_path) or os.path.islink(file_or_folder_path):
                    os.unlink(file_or_folder_path)  # Remove file or symbolic link
                elif os.path.isdir(file_or_folder_path):
                    shutil.rmtree(file_or_folder_path)  # Remove folder and its contents
            except Exception as e:
                print(f"Failed to delete {file_or_folder_path}: {e}")
        print(f"All files and folders in '{directory}' have been deleted.")
    else:
        print(f"Directory '{directory}' does not exist.")


# Example usage
# Path relative to the content root
content_root = os.getcwd()
models_directory = os.path.join(content_root, "Models")
delete_files_in_directory(models_directory)
