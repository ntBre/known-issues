.PHONY: all help

all: output/report.pdf

ifndef TARGET
    ifneq "$(MAKECMDGOALS)" "help"
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

help:
	@echo Usage:
	@echo 'make TARGET=TORSION_TARGET [FF=forcefield.offxml] [DATA="ds1,ds2,dsn"]'
