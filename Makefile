################################################################
# PieMaker: Makefile for building Python packages
# https://github.com/cliffano/piemaker
################################################################

# PieMaker info
PIEMAKER_VERSION = 2.13.0

UPDATE_GH_ID = cliffano
UPDATE_MAKEFILE = piemaker
UPDATE_GENERATOR = python
UPDATE_DOTFILES = .github/. .coveragerc .gitignore .pylintrc .rtk.json AGENTS.md
UPDATE_PARTIALS = AVATAR BADGES BUILD_REPORTS DEVELOPERS_GUIDE

################################################################
# User configuration variables
# https://github.com/cliffano/piemaker#configuration
# These variables should be stored in piemaker.yml config file,
# and they will be parsed using yq https://github.com/mikefarah/yq

# PACKAGE_NAME is the name of the Python package
PACKAGE_NAME=$(shell yq .package_name piemaker.yml)

# AUTHOR is the author of the Python package
AUTHOR ?= $(shell yq .author piemaker.yml)

$(info ################################################################)
$(info Building Python package using PieMaker with user configurations...)
$(info - Package name = ${PACKAGE_NAME})
$(info - Author = ${AUTHOR})

export POETRY_HOME := /opt/poetry
export VIRTUAL_ENV := .venv
export PATH := ${VIRTUAL_ENV}/bin:${POETRY_HOME}/bin:$(PATH)

define python_venv
	. .venv/bin/activate && $(1)
endef

################################################################
# Base targets

# CI target to be executed by CI/CD tool
all: ci
ci: clean style lint test coverage complexity doc package reinstall test-integration

# Ensure stage directory exists
stage:
	mkdir -p stage/ stage/gh-pages/

# Remove all temporary (staged, generated, cached) files
clean:
	rm -rf stage/ *.lock *.egg-info build dist/ stage/gh-pages/ $(PACKAGE_NAME)/__pycache__/ $(PACKAGE_NAME)/*.pyc tests/__pycache__/ tests/*.pyc .coverage .pytest_cache/ .tox/ .mypy_cache/ .coverage.*

# Retrieve the Pyhon package dependencies
deps:
	python3 -m venv ${POETRY_HOME} && ${POETRY_HOME}/bin/pip install --force-reinstall poetry==2.3.2 --ignore-installed
	python3 -m venv ${VIRTUAL_ENV} && PATH=${POETRY_HOME}/bin/:$$PATH poetry install --no-root --compile
	python3 -m venv ${POETRY_HOME} && ${POETRY_HOME}/bin/pip install --force-reinstall poetry-plugin-up==0.9.0 --ignore-installed
	$(call python_venv,poetry self add poetry-plugin-export)
	$(call python_venv,poetry export -f requirements.txt --without-hashes --with dev --output requirements.txt)
	$(call deps_extra)

deps-upgrade:
	$(call python_venv,poetry up --latest)

deps-extra-apt:
	apt-get update
	apt-get install -y python3-venv
	apt-get install -y python3-sphinx # needed by sphinx-apidoc
	apt-get install -y markdownlint
	$(call run_hook,x-post-deps-extra-apt)

rmdeps:
	rm -f poetry.lock requirements.txt
	rm -rf .venv/

################################################################
# Formatting targets

style:
	$(call python_venv,black $(PACKAGE_NAME) tests tests-integration examples)

################################################################
# Testing targets

lint: stage
	rm -rf stage/gh-pages/lint/pylint/ stage/lint/ && mkdir -p stage/gh-pages/lint/pylint/ stage/lint/
	$(call python_venv,pylint $(shell find $(PACKAGE_NAME) -type f -regex ".*\.py" | xargs echo) $(shell find tests/ -type f -regex ".*\.py" | xargs echo) $(shell find tests-integration/ -type f -regex ".*\.py" | xargs echo))
	$(call python_venv,pylint $(shell find $(PACKAGE_NAME) -type f -regex ".*\.py" | xargs echo) $(shell find tests/ -type f -regex ".*\.py" | xargs echo) $(shell find tests-integration/ -type f -regex ".*\.py" | xargs echo) --output-format=pylint_report.CustomJsonReporter > stage/gh-pages/lint/pylint/report.json)
	$(call python_venv,pylint_report stage/gh-pages/lint/pylint/report.json -o stage/gh-pages/lint/pylint/index.html)
	mdl -r ~MD013,~MD029 $(shell find . -path ./stage -prune -o -path ./.venv -prune -o -path ./.pytest_cache -prune -o -name "CHANGELOG.md" -prune -o -name "*.md" -print)

complexity: stage
	rm -rf stage/gh-pages/complexity/radon/ stage/complexity/ && mkdir -p stage/gh-pages/complexity/radon/ stage/complexity/
	$(call python_venv,radon mi $(PACKAGE_NAME)/) 2>&1 | tee -a stage/gh-pages/complexity/radon/report.txt
	$(call python_venv,radon cc -s -a $(PACKAGE_NAME)/) 2>&1 | tee -a stage/gh-pages/complexity/radon/report.txt
	$(call python_venv,cat stage/gh-pages/complexity/radon/report.txt | ansi2html) > stage/gh-pages/complexity/radon/index.html

test:
	rm -rf stage/gh-pages/test/pytest/ stage/test/ && mkdir -p stage/gh-pages/test/pytest/ stage/test/
	$(call python_venv,pytest -v tests --html=stage/gh-pages/test/pytest/index.html --self-contained-html --capture=no)

test-integration:
	rm -rf stage/gh-pages/test-integration/pytest/ stage/test-integration/ && mkdir -p stage/gh-pages/test-integration/pytest/ stage/test-integration/
	$(call python_venv,pytest -v tests-integration --html=stage/gh-pages/test-integration/pytest/index.html --self-contained-html --capture=no)

test-examples:
	mkdir -p stage/test-examples/
	cd examples && \
	for f in *.sh; do \
	  bash -x "$$f"; \
	done

coverage:
	rm -rf stage/gh-pages/coverage/coverage/ stage/coverage/ && mkdir -p stage/gh-pages/coverage/coverage/ stage/coverage/
	$(call python_venv,COVERAGE_FILE=.coverage.unit coverage run --source=./$(PACKAGE_NAME) -m unittest discover -s tests)
	$(call python_venv,coverage combine)
	$(call python_venv,coverage report)
	$(call python_venv,coverage html && rm -f stage/gh-pages/coverage/coverage/.gitignore)

################################################################
# Packaging, installation, and publishing targets

package:
	$(call python_venv,poetry build)

install:
	$(call python_venv,poetry install)

uninstall:
	$(call python_venv,pip3 uninstall $(PACKAGE_NAME) -y || echo "Nothing to uninstall...")

reinstall: uninstall install

publish:
	$(call python_venv,poetry publish $(if $(PASSWORD),--username __token__ --password $(PASSWORD)))

################################################################
# Documentation targets

doc: stage
	rm -rf stage/gh-pages/doc/sphinx/ stage/doc/ && mkdir -p stage/gh-pages/doc/sphinx/ stage/doc/
	$(call python_venv,sphinx-apidoc -o stage/gh-pages/doc/sphinx/ --full -H "$(PACKAGE_NAME)" -A "$(AUTHOR)" $(PACKAGE_NAME) && \
		printf "\nimport os\nimport sys\nsys.path.insert(0, os.path.abspath('../../../..'))\n" >> stage/gh-pages/doc/sphinx/conf.py && \
		cd stage/gh-pages/doc/sphinx/ && \
		make html && \
		cp -R _build/html/* .)

################################################################
# MAKE IT SO - Utility Makefile functions and targets
################################################################

define run_hook
	@if [ -f Makefile-extras ] && grep -q "^$(1):" Makefile-extras; then \
		$(MAKE) -f Makefile-extras $(1); \
	fi
endef

define deps_extra
	@if command -v apt-get > /dev/null 2>&1; then \
		if [ "$$(id -u)" = "0" ]; then \
			$(MAKE) deps-extra-apt; \
		else \
			sudo $(MAKE) deps-extra-apt; \
		fi; \
	fi
endef

define update_dotfiles_from_generator
	cd stage/ && \
	  rm -rf generator-$(1)/ && \
	  git clone https://github.com/$(UPDATE_GH_ID)/generator-$(1) && \
	  cd generator-$(1) && \
	  make deps && \
	  node_modules/.bin/plop $(UPDATE_GENERATOR_COMPONENT) -- \
	    --project_id "$(UPDATE_GENERATOR_INPUTS_PROJECT_ID)" \
		--project_name "$(UPDATE_GENERATOR_INPUTS_PROJECT_NAME)" \
		--project_desc "$(UPDATE_GENERATOR_INPUTS_PROJECT_DESC)" \
		--author_name "$(UPDATE_GENERATOR_INPUTS_AUTHOR_NAME)" \
		--author_email "$(UPDATE_GENERATOR_INPUTS_AUTHOR_EMAIL)" \
		--author_url "$(UPDATE_GENERATOR_INPUTS_AUTHOR_URL)" \
		--github_id "$(UPDATE_GENERATOR_INPUTS_GITHUB_ID)" \
		--github_repo "$(UPDATE_GENERATOR_INPUTS_GITHUB_REPO)" \
		--github_token_prefix "$(UPDATE_GENERATOR_INPUTS_GITHUB_TOKEN_PREFIX)"
	cd stage/generator-$(1)/stage/$(UPDATE_GENERATOR_COMPONENT) && \
	  for dotfile in $(2); do \
		cp -R "$$dotfile" ../../../../"$$dotfile"; \
	  done
endef

define update_partials_from_generator
	cd stage/ && \
	  rm -rf generator-$(1)/ && \
	  git clone https://github.com/$(UPDATE_GH_ID)/generator-$(1) && \
	  cd generator-$(1) && \
	  make deps && \
	  node_modules/.bin/plop $(UPDATE_GENERATOR_COMPONENT)-partials -- \
	    --project_id "$(UPDATE_GENERATOR_INPUTS_PROJECT_ID)" \
		--project_name "$(UPDATE_GENERATOR_INPUTS_PROJECT_NAME)" \
		--project_desc "$(UPDATE_GENERATOR_INPUTS_PROJECT_DESC)" \
		--author_name "$(UPDATE_GENERATOR_INPUTS_AUTHOR_NAME)" \
		--author_email "$(UPDATE_GENERATOR_INPUTS_AUTHOR_EMAIL)" \
		--author_url "$(UPDATE_GENERATOR_INPUTS_AUTHOR_URL)" \
		--github_id "$(UPDATE_GENERATOR_INPUTS_GITHUB_ID)" \
		--github_repo "$(UPDATE_GENERATOR_INPUTS_GITHUB_REPO)" \
		--github_token_prefix "$(UPDATE_GENERATOR_INPUTS_GITHUB_TOKEN_PREFIX)"
	for block in $(2); do \
	  partial_file=$$(printf "%s" "$$block" | tr "A-Z" "a-z"); \
	  ex -s \
	    -c "/<!-- BEGIN:$$block -->/+1,/<!-- END:$$block -->/-1d" \
	    -c "/<!-- BEGIN:$$block -->/r stage/generator-$(1)/stage/$(UPDATE_GENERATOR_COMPONENT)-partials/$$partial_file.txt" \
	    -c 'wq' \
	    README.md; \
	done
endef

define set_generator_vars
$(1): UPDATE_GENERATOR_COMPONENT = $$(shell yq .generator.component $(2).yml)
$(1): UPDATE_GENERATOR_INPUTS_PROJECT_ID = $$(shell yq .generator.inputs.project_id $(2).yml)
$(1): UPDATE_GENERATOR_INPUTS_PROJECT_NAME = $$(shell yq .generator.inputs.project_name $(2).yml)
$(1): UPDATE_GENERATOR_INPUTS_PROJECT_DESC = $$(shell yq .generator.inputs.project_desc $(2).yml)
$(1): UPDATE_GENERATOR_INPUTS_AUTHOR_NAME = $$(shell yq .generator.inputs.author_name $(2).yml)
$(1): UPDATE_GENERATOR_INPUTS_AUTHOR_EMAIL = $$(shell yq .generator.inputs.author_email $(2).yml)
$(1): UPDATE_GENERATOR_INPUTS_AUTHOR_URL = $$(shell yq .generator.inputs.author_url $(2).yml)
$(1): UPDATE_GENERATOR_INPUTS_GITHUB_ID = $$(shell yq .generator.inputs.github_id $(2).yml)
$(1): UPDATE_GENERATOR_INPUTS_GITHUB_REPO = $$(shell yq .generator.inputs.github_repo $(2).yml)
$(1): UPDATE_GENERATOR_INPUTS_GITHUB_TOKEN_PREFIX = $$(shell yq .generator.inputs.github_token_prefix $(2).yml)
endef

# Update Makefile to the latest version tag
update-to-latest: UPDATE_TARGET_VERSION = $(shell curl -s https://api.github.com/repos/$(UPDATE_GH_ID)/$(UPDATE_MAKEFILE)/tags | jq -r '.[0].name')
update-to-latest: update-to-version

# Update Makefile to the main branch
update-to-main:
	curl https://raw.githubusercontent.com/$(UPDATE_GH_ID)/$(UPDATE_MAKEFILE)/main/src/Makefile-$(UPDATE_MAKEFILE) -o Makefile

# Update Makefile to the version defined in UPDATE_TARGET_VERSION parameter
update-to-version:
	curl https://raw.githubusercontent.com/$(UPDATE_GH_ID)/$(UPDATE_MAKEFILE)/$(UPDATE_TARGET_VERSION)/src/Makefile-$(UPDATE_MAKEFILE) -o Makefile

# Update dotfiles using the generator
$(eval $(call set_generator_vars,update-dotfiles,$(UPDATE_MAKEFILE)))
update-dotfiles: stage
	$(call update_dotfiles_from_generator,$(UPDATE_GENERATOR),$(UPDATE_DOTFILES))
	$(call run_hook,x-post-update-dotfiles)

# Update partial snippets using the generator
$(eval $(call set_generator_vars,update-partials,$(UPDATE_MAKEFILE)))
update-partials: stage
	$(call update_partials_from_generator,$(UPDATE_GENERATOR),$(UPDATE_PARTIALS))

release-major:
	rtk release --release-increment-type major

release-minor:
	rtk release --release-increment-type minor

release-patch:
	rtk release --release-increment-type patch

################################################################

.PHONY: $(1) all ci stage clean deps deps-upgrade deps-extra-apt rmdeps style lint complexity test test-integration test-examples coverage package install uninstall reinstall publish doc update-to-latest update-to-main update-to-version update-dotfiles update-partials release-major release-minor release-patch
