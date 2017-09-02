notebooks := $(wildcard *.ipynb)
markdowns := $(patsubst %.ipynb,%.md,$(wildcard *.ipynb))
pdfs := $(patsubst %.ipynb,%.pdf,$(wildcard *.ipynb))


.DEFAULT: all
.PHONY: all
all: $(markdowns) $(pdfs)
	@echo Done

$(markdowns): $(notebooks)
	jupyter nbconvert --to markdown \"$(patsubst %.md,%.ipynb,$@)\"

$(pdfs): $(notebooks)
	jupyter nbconvert --to pdf \"$(patsubst %.pdf,%.ipynb,$@)\"

