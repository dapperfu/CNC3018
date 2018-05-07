# Config

# Makefile directory
MK_DIR = $(realpath $(dir $(firstword $(MAKEFILE_LIST))))

# Project name
PROJ ?= $(notdir ${MK_DIR})
# Virtual environment path
VENV ?= ${MK_DIR}
# Hostname
HOST:=$(shell hostname).local
# Executable paths
PIP:=${VENV}/bin/pip
PYTHON:=${VENV}/bin/python

# Base python modules to install before everything else
# Some projects need wheel, numpy and cython
# before they will install correctly.
BASE_MODULES?=pip setuptools wheel


# Bootstrap Environments



# Targets
.DEFAULT: null
.PHONY: null
null:
	$(error No default target)

.PHONY: xenial
xenial: requirements-apt.txt
		cat ${<} | sudo xargs apt-get install -y

.PHONY: develop
develop: requirements-dev.txt
	${MAKE} clean
	python3 -mvenv ${VENV}
	${PIP} install --upgrade ${BASE_MODULES}
	${PIP} install --requirement ${<}
	${PIP} install -e .


.PHONY: venv
venv: ${PYTHON}

${PYTHON}: requirements.txt
	python3 -mvenv ${VENV}
	${PIP} install --upgrade ${BASE_MODULES}
	${PIP} install --upgrade --requirement ${<}

.PHONY: clean
clean:
	@echo --- Cleaning ${PROJ} ---
	$(shell git clean -xfdn)
	git clean -xfd

requirements.txt:
	$(error ${@} is missing.)

requirements-dev.txt:
	$(error ${@} is missing.)

.PHONY:nb
nb:
	screen -S ${PROJ} -d -m bin/jupyter-notebook --ip=${HOST}

.PHONY: debug
debug:
	$(info $${MK_DIR}=${MK_DIR})
	$(info $${HOST}=${HOST})
	$(info $${PROJ}=${PROJ})
