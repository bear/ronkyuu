
venv:
ifndef VIRTUAL_ENV
	$(error Please install and activate a virtualenv before using the init or dev targets)
endif

init:
	pip install wheel
	pip install nose
	pip install check-manifest
	pip install -r requirements.txt

dev: init
	pip install --upgrade -e .

test:
	nosetests --verbosity=2 tests 

upload: check
	python setup.py sdist upload
	python setup.py bdist_wheel upload

clean:
	python setup.py clean

distclean: clean dist

dist: check
	python setup.py sdist

check:
	check-manifest
	python setup.py check
