# -*- coding: utf-8 -*-

import isort
import nbformat


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
