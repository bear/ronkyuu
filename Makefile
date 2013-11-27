
init:
	pip install -r requirements.txt

test:
	nosetests --verbosity=2 tests 
