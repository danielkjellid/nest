PACKAGE = nest
BASE 	= $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

POETRY      = poetry

V 		= 0
Q 		= $(if $(filter 1,$V),,@)
M 		= $(shell printf "\033[34;1m▶\033[0m")

###################
# Running servers #
###################

# If the first argument is "run-backend"...
ifeq (run-backend,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_BACKEND_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_BACKEND_ARGS):;@:)
endif

.PHONY: run-backend
run-backend: ; $(info $(M) Running api server...) @
	$Q cd $(BASE) && $(POETRY) run python $(BASE)/nest/main.py $(RUN_BACKEND_ARGS)


##############
# Migrations #
##############

.PHONY: migrate
migrate: ; $(info $(M) Migrating database...) @
	$Q cd $(BASE) && $(POETRY) run alembic -c nest/alembic.ini upgrade head