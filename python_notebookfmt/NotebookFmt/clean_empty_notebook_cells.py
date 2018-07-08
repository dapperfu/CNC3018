# -*- coding: utf-8 -*-

import nbformat


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

    nb["cells"] = temp_cells
    with open(notebook, "w") as fp:
        nbformat.write(nb, fp)
