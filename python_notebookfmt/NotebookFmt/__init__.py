# -*- coding: utf-8 -*-

import sys

import glob
import nbformat
import os
import black
import isort

from .clean_empty_notebook_cells import clean_empty_notebook_cells

from .isort_notebook_cells import isort_notebook_cells

from .black_notebook_cells import black_notebook_cells
from .clean_empty_notebook_cells import bubble_import_notebook_cells


cleaning_functions = list()

cleaning_functions.append(bubble_import_notebook_cells)
cleaning_functions.append(isort_notebook_cells)
cleaning_functions.append(black_notebook_cells)
cleaning_functions.append(clean_empty_notebook_cells)


def main(args=sys.argv):
    assert len(args) == 2
    for cleaning_function in cleaning_functions:
        cleaning_function(notebook=args[1])


import pkg_resources


def get_sneks():
    sneks = {}
    for entry_point in pkg_resources.iter_entry_points("snek_types"):
        sneks[entry_point.name] = entry_point.load()
    return sneks


if __name__ == "__main__":
    main()
