# LaTeX build for entropy.tex and faq.tex
MAIN = entropy
FAQ = faq
LATEX = pdflatex
LATEXFLAGS = -interaction=nonstopmode -file-line-error
BIBTEX = bibtex

.PHONY: all clean distclean faq

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex
	$(LATEX) $(LATEXFLAGS) $(MAIN)
	@if [ -f $(MAIN).bib ]; then $(BIBTEX) $(MAIN); fi
	$(LATEX) $(LATEXFLAGS) $(MAIN)
	$(LATEX) $(LATEXFLAGS) $(MAIN)

faq: $(FAQ).pdf

$(FAQ).pdf: $(FAQ).tex
	$(LATEX) $(LATEXFLAGS) $(FAQ)
	$(LATEX) $(LATEXFLAGS) $(FAQ)

clean:
	rm -f $(MAIN).aux $(MAIN).log $(MAIN).out $(MAIN).toc \
	      $(MAIN).bbl $(MAIN).blg $(MAIN).synctex.gz $(MAIN).fls $(MAIN).fdb_latexmk
	rm -f $(FAQ).aux $(FAQ).log $(FAQ).out $(FAQ).synctex.gz $(FAQ).fls $(FAQ).fdb_latexmk

distclean: clean
	rm -f $(MAIN).pdf $(FAQ).pdf
