import os
import sys

from PyQt5.uic import compileUi


def compile_ui_file(root_path, file_name):
    file_name = os.path.join(root_path, file_name)

    if file_name.endswith('.pyc'):
        os.remove(file_name)
    if not file_name.endswith('.ui'):
        return

    py_file_name = file_name.replace('.ui', '.py')

    with open(py_file_name, 'w') as py_file:
        compileUi(file_name, py_file)


if not getattr(sys, 'frozen', False):
    print('compiling ui sources')
    dir = os.path.dirname(__file__)
    for root, folders, files in os.walk(dir):
        for file in files:
            compile_ui_file(root, file)