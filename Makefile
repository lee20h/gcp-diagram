.PHONY: all check openapi clean

DIAGRAMS := $(shell find . -type f -name 'diagram.py')

all: run

run:
	$(foreach diagram,$(DIAGRAMS),python3 $(diagram);)

clean:
	@rm -rf img
