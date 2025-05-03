from fs_utils.list_files import list_files_in_directory
from parse_files.parse_python_files import read_python_file_to_text, extract_all_functions_and_methods
from agents.code_analyzer_agent import CodeAnalyzer 
from agents.code_reviewer_agent import CodeReviewer


def run():
    source_root_path = 'saras-easd-2020-retinanet'
    code_file_type = ['.py']
    python_files_path_lst = list_files_in_directory(source_root_path, code_file_type)
    model_name = 'qwen3:1.7b'
    code_analyzer_obj = CodeAnalyzer(model_name)
    code_reviewer_obj = CodeReviewer(model_name)
    for python_file_path in python_files_path_lst:
        if "anchors" not in python_file_path:
            continue
        code_as_txt = read_python_file_to_text(python_file_path)
        result_dct = extract_all_functions_and_methods(code_as_txt)
        for key, value in result_dct.items():
            classes_dct = result_dct['classes']
            functions_dct = result_dct['top_level_functions']
            for func_name, func_txt in functions_dct:
                code_documentation = code_analyzer_obj.explain_code(func_txt)
                reviewed_code_documentation = code_reviewer_obj.review_code(func_txt, code_documentation)


            print('break')

if __name__ == '__main__':
    run()