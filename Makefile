.PHONY: dev
dev:
	sudo apt-get install texlive-xetex pandoc
	sudo cp 42-cnc.rules /etc/udev/rules.d/


venv:
	python3 -mvenv venv

.PHONY: venv_init
venv_init:
	pip install -U -r requirements.txt
	cd python_gcode && python setup.py develop
	cd python_grbl && python setup.py develop
