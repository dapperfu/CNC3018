.PHONY: dev
dev:
	sudo apt-get install texlive-xetex pandoc
	sudo cp 42-cnc.rules /etc/udev/rules.d/

.PHONY: results
results:
	jupyter nbconvert --to pdf --output-dir=test_results/ *.ipynb
	jupyter nbconvert --to html --output-dir=test_results/ *.ipynb
	jupyter nbconvert --to markdown --output-dir=test_results/ *.ipynb

