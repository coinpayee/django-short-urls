#############
# VARIABLES #
#############

#----
# PLATFORM DEPENDENT
UNAME_S := $(shell sh -c 'uname -s 2>/dev/null || echo not')

ifeq (${UNAME_S}, Darwin)
	CFLAGS = CFLAGS="-I /opt/local/include -L /opt/local/lib"
endif
#-----


PROJECT_DIR := $(dir $(firstword $(MAKEFILE_LIST)))
APP_DIR = ${PROJECT_DIR}${APP_NAME}/
APP_TESTS_DIR = ${APP_DIR}tests/

WORK4CORE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
WORK4CORE_BIN = ${WORK4CORE_DIR}bin/
WORK4CORE_TESTS_DIR = ${WORK4CORE_DIR}django_app/tests/

TEMP_DIR = ${PROJECT_DIR}temp/
PYTHONHOME ?= ${PROJECT_DIR}venv
VENV_WRAPPER_DIR = $(abspath ${PYTHONHOME})/.virtualenvs/

PHANTOM_VERSION = 1.9.0

ifeq (${WORK4CORE_DIR}, ${PROJECT_DIR})
	IN_WORK4CORE_PROJECT = TRUE
else
	IN_WORK4CORE_PROJECT = FALSE
endif

ifeq (${IN_WORK4CORE_PROJECT}, TRUE)
	PW4C_DIR = ${PROJECT_DIR}
else
	PW4C_DIR = ${PROJECT_DIR}vendor/pywork4core
endif

## Specific to virtualenv
include ${WORK4CORE_DIR}/virtualenv/Makefile

RUNNER = ${ACTIVATE_VENV} &&

ifeq ($(wildcard $(PROJECT_DIR).env),)
	USE_FOREMAN = FALSE
	RUN_CMD = ${RUNNER}

	SETTINGS_TPL_FILE = ${APP_DIR}local_settings.tpl.py
	SETTINGS_FILE = ${APP_DIR}local_settings.py
else
	USE_FOREMAN = TRUE
	RUN_CMD = ${RUNNER} foreman run
	START_CMD = ${RUNNER} foreman start

	SETTINGS_TPL_FILE = ${PROJECT_DIR}env.tpl
	SETTINGS_FILE = ${PROJECT_DIR}.env
endif


##########
# CONFIG #
##########

.SILENT: deep_clean_ask confirm install install_pre install_do install_project install_post

all: clean install lint test

#########
# RULES #
#########

################
# Installation #
################

install: install_pre install_do install_project install_post

install_pre:

install_do: venv
	mkdir -p ${TEMP_DIR}

install_project::

install_phantomjs:
	./bin/install_phantomjs ${PHANTOM_VERSION}

install_post:
	echo "Copying settings..."
	([ ! -f ${SETTINGS_TPL_FILE} ] && echo "Project does not have a settings file.") || \
		([ -f ${SETTINGS_FILE} ] && echo "Settings file already exists.") || \
			(cp -n ${SETTINGS_TPL_FILE} ${SETTINGS_FILE} && vi ${SETTINGS_FILE})


######################
# Temp file handling #
######################

clean:
	(test -d ${TEMP_DIR} && rm -rf ${TEMP_DIR}* ) || true

# The code below helps reset the repository completely to its pre-install state
deep_clean: deep_clean_ask confirm deep_clean_do

deep_clean_ask:
	echo "This will remove any unversioned files, except for the settings file"

deep_clean_do: clean_pyc
	rm -rf ${TEMP_DIR} ${PYTHONHOME}

clean_pyc:
	# -print0 doesn't seem to work
	find ${PROJECT_DIR} -name "*.pyc" -or -name "*.pyo" | tr "\n" "\000" | xargs -0 rm -f


###################
# Code validation #
###################

PYLINT_RC = ${WORK4CORE_DIR}config/pylint.rc
EXTRA_ARGS_FOR_TESTS = --method-rgx='([a-z_][a-z0-9_]{2,30}|(setUp|tearDown)(Class)?)$$' --disable=C0111,R0904,C0321,W0212
lint:
	${PYTHONHOME}/bin/pep8 --config=${WORK4CORE_DIR}config/pep8.cfg ${PROJECT_DIR}
	${PYTHONHOME}/bin/pylint --rcfile=${PYLINT_RC} ${WORK4CORE_DIR}
	${PYTHONHOME}/bin/pylint --rcfile=${PYLINT_RC} ${EXTRA_ARGS_FOR_TESTS} ${WORK4CORE_TESTS_DIR}
ifeq (${IN_WORK4CORE_PROJECT}, TRUE)
else
	${PYTHONHOME}/bin/pylint --rcfile=${PYLINT_RC} ${APP_DIR}
	${PYTHONHOME}/bin/pylint --rcfile=${PYLINT_RC} ${EXTRA_ARGS_FOR_TESTS} ${APP_TESTS_DIR}
endif


#########
# Tests #
#########

COVERAGE_RC = ${WORK4CORE_DIR}config/coverage.rc

test:
	${RUN_CMD} ${PYTHONHOME}/bin/coverage run --rcfile=${COVERAGE_RC} --source=${APP_DIR},${WORK4CORE_DIR} ${PROJECT_DIR}manage.py test --traceback --noinput django_app
	${RUN_CMD} ${PYTHONHOME}/bin/coverage run --append --rcfile=${COVERAGE_RC} --source=${APP_DIR},${WORK4CORE_DIR} ${PROJECT_DIR}manage.py test --traceback --noinput ${APP_NAME}
	@${PYTHONHOME}/bin/coverage report --rcfile=${COVERAGE_RC} --fail-under=100 || (printf "\033[31mTest coverage is less than 100%%!\033[0m\n" && exit 1)

test_report:
	${PYTHONHOME}/bin/coverage html --rcfile=${COVERAGE_RC}
	${WORK4CORE_BIN}/open ${TEMP_DIR}/coverage_html/index.html

test_and_report:
	(make test || make test_report) | grep -vE '100\%$$'

################################
# Running the app and commands #
################################

run:
	${RUN_CMD} ${PROJECT_DIR}manage.py runserver

ifeq (${USE_FOREMAN}, TRUE)
start:
	${START_CMD} $(PROC)
endif

shell:
	${RUN_CMD} ${PROJECT_DIR}manage.py shell

collectstatic:
	${RUN_CMD} ${PROJECT_DIR}manage.py collectstatic --noinput


##########################
# Git Subtree Management #
##########################

ifeq (${IN_WORK4CORE_PROJECT}, TRUE)
	# Git subtree commands cannot be run from the PyWork4Core project
else
git-subtree = git subtree ${1} --prefix=vendor/pywork4core --squash pywork4core master

git_subtree_pull:
	$(call git-subtree, pull)

git_subtree_push:
	$(call git-subtree, push)
endif

###########
# Helpers #
###########

confirm:
	${WORK4CORE_BIN}/confirm

PASS:
