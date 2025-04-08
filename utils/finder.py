import os
def get_file_path_from_output(filename: str, output_dir: str = "output") -> str | None:
    """
    Searches for the given filename inside the output directory.
    Returns the full path if found, else None.
    """
    for file in os.listdir(output_dir):
        if file == filename:
            return os.path.join(output_dir, file)
    return None