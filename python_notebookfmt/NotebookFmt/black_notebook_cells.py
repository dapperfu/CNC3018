# -*- coding: utf-8 -*-

import black
import nbformat


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
                code_cell["source"], line_length=80
            )
        except:
            print("Failed: {}".format(code_cell["source"]))

    with open(notebook, "w") as fp:
        nbformat.write(nb, fp)
