from setuptools import setup

setup(
    name="NotebookFmt",
    version="0.1",
    description="NotebookFmt",
    author="Jed Frey",
    license="BSD",
    packages=["NotebookFmt"],
    entry_points={
        "console_scripts": ["notebookformat=NotebookFmt:main"],
        "snek_types": ["clean_empty=NotebookFmt:clean_empty_notebook_cells"],
    },
    zip_safe=False,
)
