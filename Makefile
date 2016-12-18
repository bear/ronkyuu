help:
	@echo "  env         install all production dependencies"
	@echo "  dev         install all dev and production dependencies (virtualenv is assumed)"
	@echo "  clean       remove unwanted stuff"
	@echo "  lint        check style with pycodestyle"
	@echo "  test        run tests"
	@echo "  coverage    run codecov"

env:
	pyenv install -s 2.7.12
	pyenv install -s 3.5.2
	pyenv local 2.7.12 3.5.2
	pip install -U pip

dev: env
	pip install -Ur requirements.txt
	pip install -Ur requirements-test.txt

info:
	@python --version
	@pyenv --version
	@pip --version
	@pycodestyle --version

clean:
	rm -rf build
	rm -rf dist
	rm -f violations.flake8.txt
	python setup.py clean
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' ! -name '*.un~' -exec rm -f {} \;

lint: info
	pycodestyle

test: lint
	python setup.py test

tox.ini: requirements.txt requirements-test.txt
	tox --recreate

tox: tox.ini
	tox

coverage: clean
	coverage run --source=ronkyuu setup.py test

ci: lint coverage
	@coverage html
	@coverage report
	# CODECOV_TOKEN=`cat .codecov-token` codecov

check: clean
	check-manifest
	python setup.py check

upload: check
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: check
	python setup.py sdist
