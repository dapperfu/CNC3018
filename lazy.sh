#!/bin/sh

# Make sure your venv is not a subfolder of where this is run.
git commit -am "Prelazy"
find . -name "*.py" | xargs -n1 -P8 black --py36 --line-length 80
find . -name "*.ipynb" | xargs -n1 -P8 notebookcleaner
git commit -am "Postlazy"
