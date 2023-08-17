.PHONY: all help script

all: output/report.pdf

ifndef TARGET
    ifeq "$(MAKECMDGOALS)" "all"
	$(error must specify a TARGET)
    endif
endif

flags :=

ifdef FF
    flags += --forcefield $(FF)
endif

ifdef DATA
    comma := ,
    flags += --dataset $(subst $(comma),--dataset ,$(DATA))
endif

ifdef PLOT
    flags += --plot-torsions
endif

TEXFLAGS = -output-directory=output -halt-on-error

output/report.pdf: output/report.tex
	pdflatex $(TEXFLAGS) $^
ifdef OPEN
	$(OPEN) $@
endif

output/report.tex: main.py latex.py
	rm -rf output
	mkdir -p output
	python main.py --target $(TARGET) $(flags)

script: output/report.tex

# rows and columns in montage
LAYOUT ?= +5+3
output/plots.png: $(wildcard output/plot*.png)
	montage $^ -geometry 400x300\>$(LAYOUT) $@

help:
	@echo Usage:
	@echo 'make TARGET=TORSION_TARGET [FF=forcefield.offxml] [DATA="ds1,ds2,dsn"] [PLOT=1]'

output/montage.png: output/report.pdf Makefile
	pdfseparate $< 'output/page%02d.pdf'
	for page in output/page*.pdf; do \
		b=$$(basename $$page); \
		name=output/$${b%.pdf}.png; \
		convert -density 300 -trim $$page -quality 100 $$name; \
	done
	size=$$(file output/page01.png | sed -En 's/.* ([0-9]+) x ([0-9]+),.*/\1x\2/p'); \
	montage output/page*.png -tile 4x -geometry $$size+100+100\> $@
