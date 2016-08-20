help:
	@echo "  env         install all production dependencies"
	@echo "  dev         install all dev and production dependencies (virtualenv is assumed)"
	@echo "  clean       remove unwanted stuff"
	@echo "  lint        check style with flake8"
	@echo "  test        run tests"
	@echo "  coverage    run codecov"

env:
	pip install -U pip
	pip install -Ur requirements.txt
	pip install -Ur requirements-test.txt

dev: env
	pyenv install -s 2.7.11
	pyenv install -s 3.5.2
	pyenv local 2.7.11 3.5.2

info:
	@python --version
	@pyenv --version
	@pip --version

clean:
	rm -rf build
	rm -rf dist
	rm -f violations.flake8.txt
	python setup.py clean
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' ! -name '*.un~' -exec rm -f {} \;

lint: info
	flake8 . > violations.flake8.txt

test: lint
	python setup.py test

tox: clean
	tox

coverage: clean
	coverage run --source=ronkyuu setup.py test
	coverage html
	coverage report

ci: tox coverage
	CODECOV_TOKEN=`cat .codecov-token` codecov

check: clean
	check-manifest
	python setup.py check

upload: check
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: check
	python setup.py sdist
