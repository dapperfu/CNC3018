# Config

## Targets
# Do nothing.
.PHONY: null
null:
	@$(error No Default Target).

## make_sandwich includes
# https://github.com/jed-frey/make_sandwich
include .mk_inc/env.mk
