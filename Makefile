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
	$Q cd $(BASE) && $(POETRY) run python $(BASE)/$(PACKAGE)/main.py $(RUN_BACKEND_ARGS)


##############
# Migrations #
##############

.PHONY: migrate
migrate: ; $(info $(M) Migrating database...) @
	$Q cd $(BASE) && $(POETRY) run alembic -c $(PACKAGE)/alembic.ini upgrade head


###########
# Linting #
###########

# Linters
.PHONY: lint
lint: lint-backend | $(BASE) ; @
	$Q

.PHONY: lint-backend
lint-backend: lint-ruff lint-mypy lint-black | $(BASE) ; @
	$Q

.PHONY: lint-ruff
lint-ruff: ; $(info $(M) running ruff...) @
	$Q cd $(BASE) && $(POETRY) run ruff $(PACKAGE)

.PHONY: lint-mypy
lint-mypy: ; $(info $(M) running mypy...) @
	$Q cd $(BASE) && $(POETRY) run mypy --show-error-code --show-column-numbers $(PACKAGE)

.PHONY: lint-black
lint-black: ; $(info $(M) running black...) @
	$Q cd $(BASE) && $(POETRY) run black --check $(PACKAGE)


# Fixers
.PHONY: fix
fix: fix-backend | $(BASE) ; @
	$Q

.PHONY: fix-backend
fix-backend: fix-ruff fix-black | $(BASE) ; @
	$Q

.PHONY: fix-ruff
fix-ruff: ; $(info $(M) running ruff with fix...) @
	$Q cd $(BASE) && $(POETRY) run ruff $(PACKAGE) --fix

.PHONY: fix-black
fix-black: ; $(info $(M) running black with fix...) @
	$Q cd $(BASE) && $(POETRY) run black $(PACKAGE)