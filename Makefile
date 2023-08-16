.PHONY: all help

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

# rows and columns in montage
LAYOUT ?= +5+3
output/plots.png: $(wildcard output/plot*.png)
	montage $^ -geometry 400x300\>$(LAYOUT) $@

help:
	@echo Usage:
	@echo 'make TARGET=TORSION_TARGET [FF=forcefield.offxml] [DATA="ds1,ds2,dsn"] [PLOT=1]'
