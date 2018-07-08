# -*- coding: utf-8 -*-

import nbformat


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
    import_cell["source"] = "\n".join(imports)
    nb["cells"].insert(0, import_cell)
    with open(notebook, "w") as fp:
        nbformat.write(nb, fp)
