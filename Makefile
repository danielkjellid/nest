PACKAGE 			= nest
TESTS				= tests
BASE 				= $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

POETRY      		= poetry
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

.PHONY: start
start: ; $(info $(M) Generating frontend types from schema...) @
	$Q cd $(BASE) && mprocs


###########
# Schemas #
###########

.PHONY: schema
schema: schema-backend schema-frontend | $(BASE) ; @
	$Q

.PHONY: schema-backend
schema-backend: ; $(info $(M) Exporting backend schema...) @
	$Q cd $(BASE) && $(POETRY) run python manage.py export_schema --output "$(BASE)/schema.json"

.PHONY: schema-frontend
schema-frontend: ; $(info $(M) Generating frontend types from schema...) @
	$Q cd $(BASE) && $(NPM) run openapi:generate

###########
# Linting #
###########

# Linters
.PHONY: lint
lint: lint-backend lint-frontend | $(BASE) ; @
	$Q

.PHONY: lint-backend
lint-backend: lint-mypy lint-ruff lint-ruff-format | $(BASE) ; @
	$Q

.PHONY: lint-frontend
lint-frontend: lint-tsc lint-eslint lint-prettier | $(BASE) ; @
	$Q

.PHONY: lint-ruff
lint-ruff: ; $(info $(M) running ruff lint...) @
	$Q cd $(BASE) && $(POETRY) run ruff $(PACKAGE) $(TESTS)

.PHONY: lint-ruff-format
lint-ruff-format: ; $(info $(M) running ruff format...) @
	$Q cd $(BASE) && $(POETRY) run ruff format $(PACKAGE) $(TESTS) --check

.PHONY: lint-mypy
lint-mypy: ; $(info $(M) running mypy...) @
	$Q cd $(BASE) && $(POETRY) run mypy --show-error-code --show-column-numbers $(PACKAGE)

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
fix-backend: fix-ruff .fix-ruff-format | $(BASE) ; @
	$Q

.PHONY: fix-frontend
fix-frontend: fix-eslint fix-prettier | $(BASE) ; @
	$Q

.PHONY: fix-ruff
fix-ruff: ; $(info $(M) running ruff with fix...) @
	$Q cd $(BASE) && $(POETRY) run ruff $(PACKAGE) $(TESTS) --fix

.PHONY: fix-ruff-format
.fix-ruff-format: ; $(info $(M) running ruff format with fix...) @
	$Q cd $(BASE) && $(POETRY) run ruff format $(PACKAGE) $(TESTS)

.PHONY: fix-eslint
fix-eslint: ; $(info $(M) running eslint with fix...) @
	$Q cd $(BASE) && $(NPM) run eslint:fix

.PHONY: fix-prettier
fix-prettier: ; $(info $(M) running prettier with fix...) @
	$Q cd $(BASE) && $(NPM) run prettier:fix
