import os
import glob
import os
import shutil



def list_files_in_directory(directory, file_type_lst=None):
    """
    List files in a directory with optional filtering by file types.

    Parameters:
        - directory (str): The path to the directory.
        - file_type_lst (list): List of file types to filter (e.g., ['jpeg', 'jpg', 'png']).

    Returns:
        List of file paths.
    """
    if file_type_lst:
        file_types_lower = [file_type.lower() for file_type in file_type_lst]
        files = [
            f
            for f in glob.glob(os.path.join(directory, "**"), recursive=True)
            if os.path.isfile(f) and any(f.lower().endswith(f_type) for f_type in file_types_lower)
        ]
    else:
        files = [f for f in glob.glob(os.path.join(directory, "*"), recursive=True) if os.path.isfile(f)]

    return files