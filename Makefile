### Config
VENV=_${PROJ}

## Environment
# Setup the local environment
ENVS:=python

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
lazy: README.md
	${MAKE} test.python
	${MAKE} git.sprintcommit

.PHONY: README.md
README.md:
	touch ${@}

.PHONY:nb
nb:
	screen -S ${PROJ} -d -m bin/jupyter-notebook --ip=${HOST}

