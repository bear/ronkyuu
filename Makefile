help:
	@echo "  env         install all dependencies"
	@echo "  dev         install all development dependencies"
	@echo "  clean       remove unwanted stuff"
	@echo "  lint        lint with flake8"
	@echo "  test        run tests"
	@echo "  coverage    run codecov"

clean:
	rm -rf build
	rm -rf dist
	rm -f violations.flake8.txt
	pipenv clean

dev:
	pipenv install --dev

env: clean
	pipenv install

info: env
	@pipenv run python --version
	@pipenv check
	@pipenv graph

lint: dev
	pipenv run flake8 --tee --output-file=violations.flake8.txt

test: lint
	pipenv install "-e ."
	pipenv run pytest

coverage: clean
	pipenv install "-e ."
	pipenv run coverage run -m pytest
	pipenv run coverage report
	pipenv run coverage html
	pipenv run codecov

check: env
	pipenv run check-manifest -v

dist: check
	pipenv run python -m build

upload: dist
	pipenv run python -m twine upload --repository testpypi dist/*

upload-prod: dist
	pipenv run python -m twine upload dist/*
