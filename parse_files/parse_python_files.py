import os 
import ast


def read_python_file_to_text(file_path):
    """
    Reads the content of a Python (.py) file and returns it as a string.

    Parameters:
        - file_path (str): Path to the .py file.

    Returns:
        str: Content of the file as text.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a .py file.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not file_path.lower().endswith(".py"):
        raise ValueError(f"Invalid file type: {file_path} is not a .py file")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    return content

def extract_all_functions_and_methods(code: str):
    tree = ast.parse(code)
    #lines = code.strip("\n").splitlines()
    lines = code.splitlines()
    result = {
        "classes": {},
        "top_level_functions": {}
    }

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            class_methods = {}
            for method in node.body:
                if isinstance(method, ast.FunctionDef):
                    method_start = method.lineno - 1
                    method_end = method.end_lineno
                    method_code = "\n".join(lines[method_start:method_end])
                    class_methods[method.name] = method_code
            result["classes"][class_name] = class_methods

        elif isinstance(node, ast.FunctionDef):
            function_start = node.lineno - 1
            function_end = node.end_lineno
            function_code = "\n".join(lines[function_start:function_end])
            result["top_level_functions"][node.name] = function_code

    return result