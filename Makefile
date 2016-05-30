help:
	@echo "  env         install all production dependencies"
	@echo "  dev         install all dev and production dependencies (virtualenv is assumed)"
	@echo "  clean       remove unwanted stuff"
	@echo "  lint        check style with flake8"
	@echo "  test        run tests"
	@echo "  coverage    run codecov"

env:
ifndef VIRTUAL_ENV
	$(error Please install and activate a virtualenv before using the init or dev targets)
else
	pip install -r requirements.txt
endif

dev: env
	pip install -r requirements-test.txt

update:
	pip install -r requirements.txt

info:
	python --version
	pyenv --version
	pip --version

lint:
	flake8 . > violations.flake8.txt

test: lint
	python setup.py test

coverage: clean
	coverage run --source=ronkyuu setup.py test
	coverage html
	coverage report

upload: check
	python setup.py sdist upload
	python setup.py bdist_wheel upload

clean:
	rm -rf build
	rm -rf dist
	rm -f violations.flake8.txt
	python setup.py clean
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' ! -name '*.un~' -exec rm -f {} \;

distclean: clean dist

dist: check
	python setup.py sdist

check:
	check-manifest
	python setup.py check
