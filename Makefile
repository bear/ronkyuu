help:
	@echo "  env         install all production dependencies"
	@echo "  clean       remove unwanted stuff"
	@echo "  lint        check style with pycodestyle"
	@echo "  test        run tests"
	@echo "  coverage    run codecov"

env:
	pipenv install -d

info:
	@pipenv run python --version
	@pipenv graph

clean:
	rm -rf build
	rm -rf dist
	rm -f violations.flake8.txt
	pipenv clean
	pipenv run python setup.py clean
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' ! -name '*.un~' -exec rm -f {} \;

lint: 
	pipenv run pylint --rcfile=./setup.cfg ronkyuu tests

test: lint
	pipenv run python setup.py test

coverage: clean
	pipenv run coverage run --source=ronkyuu setup.py test
	pipenv run coverage report
	pipenv run coverage html
	pipenv run codecov

check: clean
	pipenv run check-manifest
	pipenv run python setup.py check

upload: dist
	pipenv run python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

dist: check
	pipenv run python setup.py sdist bdist_wheel
