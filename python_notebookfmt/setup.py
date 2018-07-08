from setuptools import setup

setup(
    name="NotebookFmt",
    version="0.1",
    description="NotebookFmt",
    author="Jed Frey",
    license="BSD",
    packages=["NotebookFmt"],
    entry_points = {
        'console_scripts': ['notebookformat=NotebookFmt.__init__:main'],
        'snek_types': [
            'cute = cute_snek:cute_snek',
        ],
    },
    zip_safe=False,
)
