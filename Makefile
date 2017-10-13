CWD = $(realpath $(dir $(firstword $(MAKEFILE_LIST))))
VENV=.venv

.PHONY: dev
dev:
	sudo apt-get install texlive-xetex pandoc
	sudo cp 42-cnc.rules /etc/udev/rules.d/

.PHONY:venv
venv: ${VENV}

${VENV}:
	python3 -mvenv ${CWD}/${@}

	${CWD}/${VENV}/bin/pip install -U pip setuptools wheel
	${CWD}/${VENV}/bin/pip install -U -r requirements.txt
	cd python_gcode && ${CWD}/${VENV}/bin/python setup.py develop
	cd python_grbl && ${CWD}/${VENV}/bin/python setup.py develop

.PHONY: nb
nb: ${VENV}
	${CWD}/.venv/bin/jupyter-notebook

.PHONY: grbl
grbl:
	avrdude -p atmega328p -P /dev/cnc_3018 -b 57600 -c arduino -U flash:w:grbl_v1.1f.20170801.hex

.PHONY: clean
clean:
	rm -rf ${VENV}
