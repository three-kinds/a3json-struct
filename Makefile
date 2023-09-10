SHELL := /bin/bash

PACKAGE = a3json_struct

init:
	pip3 install -r requirements.txt

coverage:
	coverage erase
	coverage run -m unittest discover
	coverage html --title="$(PACKAGE) coverage report"
	python -m webbrowser ./htmlcov/index.html

test: coverage

sdist:
	python setup.py sdist

clean:
	rm -rf build dist .egg *.egg-info

upload:
	twine upload dist/* --verbose

package: sdist upload clean
