
venv:
ifndef VIRTUAL_ENV
	$(error Please install and activate a virtualenv before using the init or dev targets)
endif

init:
	pip install -r requirements.txt
	pip install -r requirements-test.txt

update:
	pip install -r requirements.txt

lint:
	flake8 . > violations.flake8.txt

test:
	nosetests --verbosity=2 tests

upload: check
	python setup.py sdist upload
	python setup.py bdist_wheel upload

clean:
	python setup.py clean
	rm -f violations.flake8.txt

distclean: clean dist

dist: check
	python setup.py sdist

check:
	check-manifest
	python setup.py check
