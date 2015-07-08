SUBDIRS := $(wildcard */.)

all:
	$(foreach var,${SUBDIRS}, $(MAKE) -C ${var};)
