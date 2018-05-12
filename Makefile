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

ARTIFACT_PTR=$(wildcard artifacts/*.txt)
ARTIFACT_FILES=$(patsubst %.txt,%,${ARTIFACT_PTR})

.PHONY: artifacts
artifacts: ${ARTIFACT_FILES}

.PHONY: ${ARTIFACT_FILES}
${ARTIFACT_FILES}:
	curl --silent --location --output "${@}" "$(shell cat "${@}.txt")"

# Lazy - Because I'm lazy.
#
# Do something I'm too lazy to do at this point in development.
.PHONY: lazy
lazy:
	${MAKE} test.python
	${MAKE} git.sprintcommit
	
.PHONY: env
env: env.python env.arduino
	
## make_sandwich includes
# https://xkcd.com/149/
# https://www.explainxkcd.com/wiki/index.php/149:_Sandwich
# https://github.com/jed-frey/make_sandwich

include .mk_inc/env.mk
