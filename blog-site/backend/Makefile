SHELL = /bin/bash
MODULE = example_backend


version:
	@poetry version -s


clean:
	-rm -rf build
	-rm -rf dist
	-rm -rf *.egg-info
	-find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf


lint:
	@echo
	@echo --- Lint ---
	pre-commit run --all-files


format:
	@echo
	@echo --- Lint ---
	pre-commit run --all-files


test-only:
	@echo
	@echo --- Test ---
	coverage run --source=example_backend -m pytest tests/
	coveralls --service=github

test: lint test-only


start: export FLASK_ENV=development
start: export FLASK_APP=start-app.py

start:
	@echo
	@echo --- Starting local server ---
	poetry run ./entrypoint.sh

.PHONY: clean lint test start
