## make_sandwich includes
# https://xkcd.com/149/
# https://www.explainxkcd.com/wiki/index.php/149:_Sandwich
# https://github.com/jed-frey/make_sandwich
include .mk_inc/env.mk

### Local Targets

# Download artifacts.
ARTIFACT_PTR=$(wildcard artifacts/*.txt)
ARTIFACT_FILES=$(patsubst %.txt,%,${ARTIFACT_PTR})
.PHONY: artifacts
artifacts: ${ARTIFACT_FILES}

.PHONY: ${ARTIFACT_FILES}
${ARTIFACT_FILES}:
	curl --silent --location --output "${@}" "$(shell cat "${@}.txt")"

.PHONY: upload
upload: artifacts/grbl_v1.1f.20170801.hex
	avrdude -p atmega328p -P /dev/cnc_3018 -b 57600 -c arduino -U flash:w:$(realpath ${<})

# Lazy - Because I'm lazy.
#
# Do something I'm too lazy to do at this point in development.
.PHONY: lazy
lazy:
	git fetch --all --verbose
	${MAKE} test.python
	${MAKE} git.sprintcommit

## Environment
# Setup the local environment
ENVS:=python
