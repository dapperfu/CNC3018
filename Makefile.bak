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

# Targets
.DEFAULT: null
.PHONY: null
null:
	$(error No default target)

# Bootstrap Environments
.PHONY: ubuntu
ubuntu:
	${MAKE} `lsb_release --short --codename`
	
.PHONY: freebsd
freebsd:
	${MAKE} `uname -r`


.PHONY: xenial
xenial: requirements-apt.txt
	cat ${<} | sudo xargs apt-get install -y
	
.PHONY: requirements-pkg.txt
	cat ${<} | xargs pkg install -y
	
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
	git clean -xfd

requirements.txt:
	$(error ${@} is missing.)

requirements-dev.txt:
	$(error ${@} is missing.)

.PHONY:nb
nb:
	screen -S ${PROJ} -d -m bin/jupyter-notebook --ip=${HOST}

.PHONY:screen
screen:
	screen -Dr ${PROJ}

.PHONY: upload
upload: grbl_v1.1f.20170801.hex
	avrdude -p atmega328p -P /dev/cnc_3018 -b 57600 -c arduino -U flash:w:${<}

grbl_v1.1f.20170801.hex:
	curl -OL https://github.com/gnea/grbl/releases/download/v1.1f.20170801/grbl_v1.1f.20170801.hex
