.PHONY: dev
dev:
	sudo apt-get install texlive-xetex pandoc
	sudo cp 42-cnc.rules /etc/udev/rules.d/

