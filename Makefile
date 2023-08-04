PACKAGE 		= nest
BASE 				= $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

POETRY      = poetry
NPM 				= npm

V 					= 0
Q 					= $(if $(filter 1,$V),,@)
M 					= $(shell printf "\033[34;1m▶\033[0m")

$(POETRY): ; $(info $(M) checking poetry...)
	$Q

$(NPM): ; $(info $(M) checking npm...)

$(BASE): | $(POETRY) $(YARN) ; $(info $(M) checking project...)
	$Q

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
run-backend: ; $(info $(M) Running api deveopment server...) @
	$Q cd $(BASE) && $(POETRY) run python $(BASE)/$(PACKAGE)/main.py $(RUN_BACKEND_ARGS)

.PHONY: run-frontend
run-frontend: ; $(info $(M) Running frontend development server...) @
	$Q cd $(BASE) && $(YARN) dev


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
lint: lint-backend lint-frontend | $(BASE) ; @
	$Q

.PHONY: lint-backend
lint-backend: lint-mypy lint-ruff lint-black | $(BASE) ; @
	$Q

.PHONY: lint-frontend
lint-frontend: lint-tsc lint-eslint lint-prettier lint-import-sort | $(BASE) ; @
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

.PHONY: lint-import-sort
lint-import-sort: ; $(info $(M) running import-sort...) @
	$Q cd $(BASE) && $(NPM) run import-sort:check

.PHONY: lint-eslint
lint-eslint: ; $(info $(M) running eslint...) @
	$Q cd $(BASE) && $(NPM) run eslint:check

.PHONY: lint-prettier
lint-prettier: ; $(info $(M) running prettier...) @
	$Q cd $(BASE) && $(NPM) run prettier:check

.PHONY: lint-tsc
lint-tsc: ; $(info $(M) running tsc...) @
	$Q cd $(BASE) && $(NPM) run tsc:check

# Fixers
.PHONY: fix
fix: fix-backend fix-frontend | $(BASE) ; @
	$Q

.PHONY: fix-backend
fix-backend: fix-ruff fix-black | $(BASE) ; @
	$Q

.PHONY: fix-frontend
fix-frontend: fix-eslint fix-prettier fix-import-sort | $(BASE) ; @
	$Q

.PHONY: fix-ruff
fix-ruff: ; $(info $(M) running ruff with fix...) @
	$Q cd $(BASE) && $(POETRY) run ruff $(PACKAGE) --fix

.PHONY: fix-black
fix-black: ; $(info $(M) running black with fix...) @
	$Q cd $(BASE) && $(POETRY) run black $(PACKAGE)

.PHONY: fix-eslint
fix-eslint: ; $(info $(M) running eslint with fix...) @
	$Q cd $(BASE) && $(NPM) run eslint:fix

.PHONY: fix-prettier
fix-prettier: ; $(info $(M) running prettier with fix...) @
	$Q cd $(BASE) && $(NPM) run prettier:fix

.PHONY: fix-import-sort
fix-import-sort: ; $(info $(M) running import-sort with fix...) @
	$Q cd $(BASE) && $(NPM) run import-sort:fix