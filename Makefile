plat := $(shell uname -s)
ifeq ($(plat), Darwin)
        mathbase = ~/Library/Mathematica/Applications/
endif
ifeq ($(plat), Linux)
	mathbase = ~/.Mathematica/Applications/
endif

all: depend math-iface

clean: clean-math-iface

# build dependencies
depend:
	sh dependencies/build-deps-sh

math-iface:
	cp mathematica/nanoporeAnalysis.m ${mathbase}
	cp mathematica/Util.m ${mathbase}

tests:
	sh install-test-sh
	
dist:
	python setup.py sdist
	sh pyinstaller-sh

distclean:
	rm -rf pyinstaller/dist/*
	rm -rf pyinstaller/build/
		

clean-math-iface:
	rm ${mathbase}/nanoporeAnalysis.m
	rm ${mathbase}/Util.m
	
