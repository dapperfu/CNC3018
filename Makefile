# Config
## Targets
# null - Do nothing.
# 
# Default target when called from ```make```.
# Explicit is better than implicit, specify your target.
# 
.PHONY: null
null:
	@$(error No Default Target).

# Lazy - Because I'm lazy.
#
# Do something I'm too lazy to do at this point in development.
.PHONY: lazy
lazy:
	nohup geany ${SANDWICH_DIR}/*.mk &

## make_sandwich includes
# https://xkcd.com/149/
# https://www.explainxkcd.com/wiki/index.php/149:_Sandwich
# https://github.com/jed-frey/make_sandwich

include .mk_inc/env.mk
