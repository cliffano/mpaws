export POETRY_HOME := /opt/poetry
export VIRTUAL_ENV := /opt/poetry-venv
export PATH := ${VIRTUAL_ENV}/bin:${POETRY_HOME}/bin:$(PATH)

ci: clean deps lint test coverage complexity doc package reinstall test-integration

# Exclude complexity due to complexity requiring no uncommited local change
dev: clean deps-extra deps lint test coverage doc package reinstall test-integration

clean:
	rm -rf stage *.egg-info build dist docs/ mpaws/_pycache_/ mpaws/*.pyc tests/_pycache_/ tests/*.pyc .coverage

stage:
	mkdir -p stage stage/ docs/

deps:
	python3 -m venv ${POETRY_HOME} && ${POETRY_HOME}/bin/pip install poetry --ignore-installed
	python3 -m venv ${VIRTUAL_ENV} && PATH=${POETRY_HOME}/bin/:$$PATH poetry install --no-root --compile

deps-extra:
	apt-get update
	apt-get install -y python3-venv

doc: stage
	rm -rf docs/doc/sphinx/ && mkdir -p docs/doc/sphinx/
	sphinx-apidoc -o stage/doc/sphinx/ --full -H "mpaws" -A "Cliffano Subagio" mpaws && \
		cd stage/doc/sphinx/ && \
		make html && \
		cp -R _build/html/* ../../../docs/doc/sphinx/

release-major:
	rtk release --release-increment-type major

release-minor:
	rtk release --release-increment-type minor

release-patch:
	rtk release --release-increment-type patch

lint: stage
	mkdir -p stage/lint/pylint/ docs/lint/pylint/
	pylint mpaws/*.py tests/*.py tests-integration/*.py
	pylint mpaws/*.py tests/*.py tests-integration/*.py --output-format=pylint_report.CustomJsonReporter > stage/lint/pylint/report.json
	pylint_report stage/lint/pylint/report.json -o docs/lint/pylint/index.html

complexity: stage
	wily build mpaws/
	wily report docs/complexity/wily/index.html

test:
	pytest -v tests --html=docs/test/pytest/index.html --self-contained-html

test-integration:
	rm -rf stage/test-integration/ && mkdir -p stage/test-integration/
	python3 -m unittest tests-integration/*.py
	cd examples/ && \
	  ./multi-profiles-multi-regions.sh || echo "" && \
		./multi-profiles-single-region.sh || echo "" && \
		./warnings.sh || echo ""

coverage:
	COVERAGE_FILE=.coverage.unit coverage run --source=./mpaws -m unittest discover -s tests
	coverage combine
	coverage report
	coverage html

install: package
	poetry install

uninstall:
	pip3 uninstall mpaws -y

reinstall:
	make uninstall || echo "Nothing to uninstall..."
	make clean deps package install

package:
	poetry build

publish:
	poetry publish --username __token__ --password $(PASSWORD)

.PHONY: ci dev clean stage deps deps-extra doc release lint complexity test test-integration coverage install uninstall reinstall package publish
