# -*- coding: utf-8 -*-

import sys

import glob
import nbformat
import os
import black
import isort

def isort_notebook_cells(notebook):
    with open(notebook, "rb") as fp:
        nb = nbformat.read(fp=fp, as_version=nbformat.NO_CONVERT)

    markdown_cells = list()
    code_cells = list()

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            code_cells.append(cell)
        elif cell["cell_type"] == "markdown":
            markdown_cells.append(cell)
        else:
            raise Exception(cell["cell_type"])

    for code_cell in code_cells:
        if code_cell["source"] == "":
            continue
        if "import" in code_cell["source"]:
            s = isort.SortImports(file_contents=code_cell.source)
            code_cell.source = s.output.strip()

    with open(notebook, "w") as fp:
        nbformat.write(nb, fp)
        
def black_notebook_cells(notebook=None):
    with open(notebook, "rb") as fp:
        nb = nbformat.read(fp=fp, as_version=nbformat.NO_CONVERT)

    markdown_cells = list()
    code_cells = list()

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            code_cells.append(cell)
        elif cell["cell_type"] == "markdown":
            markdown_cells.append(cell)
        else:
            raise Exception(cell["cell_type"])

    for code_cell in code_cells:
        if code_cell["source"] == "":
            continue
        try:
            code_cell["source"] = black.format_str(
                code_cell["source"],
                line_length=80
            )
        except:
            print("Failed: {}".format(code_cell["source"]))
            
    with open(notebook, "w") as fp:
        nbformat.write(nb, fp)
        
def clean_empty_notebook_cells(notebook):
    """ bubble imports to the top of a notebook"""
    with open(notebook, "rb") as fp:
        nb = nbformat.read(fp=fp, as_version=nbformat.NO_CONVERT)
    
    temp_cells = list()
       
    for cell in nb["cells"]:
        if cell["source"] == "":
            continue
        # Other side of the Valley.
        temp_cells.append(cell)

    nb["cells"]= temp_cells
    with open(notebook, "w") as fp:
        nbformat.write(nb, fp)
        
def bubble_import_notebook_cells(notebook):
    """ bubble imports to the top of a notebook"""
    with open(notebook, "rb") as fp:
        nb = nbformat.read(fp=fp, as_version=nbformat.NO_CONVERT)

    markdown_cells = list()
    code_cells = list()
    imports = list()
    
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            code_cells.append(cell)
        elif cell["cell_type"] == "markdown":
            markdown_cells.append(cell)
        else:
            raise Exception(cell["cell_type"])

    for code_cell in code_cells:
        if code_cell["source"] == "":
            continue
        if "import" in code_cell["source"]:
            tmp_buffer = list()
            for line in code_cell["source"].splitlines():
                if "import" in line:
                    imports.append(line)
                else:
                    tmp_buffer.append(line)
            code_cell["source"] = tmp_buffer
    import_cell = nbformat.v4.new_code_cell()
    import_cell["source"]="\n".join(imports)
    nb["cells"].insert(0, import_cell)
    with open(notebook, "w") as fp:
        nbformat.write(nb, fp)

def main(args=sys.argv):    
    assert(len(args)==2)
    
if __name__ == "__main__":
    main()
    
    
    