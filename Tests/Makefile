SRC = $(wildcard *.ipynb)
PDF = $(SRC:.ipynb=.pdf)
MD  = $(SRC:.ipynb=.md)

.DEFAULT: all
.PHONY: all
all: $(PDF) $(MD)
	@echo Done

.PHONY: clean
clean:
	@rm -rf $(PDF) $(MD) *_files

%.pdf: %.ipynb
	jupyter nbconvert --to pdf $<

%.md: %.ipynb
	jupyter nbconvert --to markdown $<
