.PHONY: docs
docs:
	rm -r docs/
	pdoc --html audl
	mv html/ docs/

clean:
	rm -r dist/
	rm -r audl.egg-info/

.PHONY: tests
tests:
	python3 -m unittests tests/stats/endpoints/*

deploy:
	# rm -r dist/
	# rm -r audl.egg-info/
	python3 -m build
	twine upload dist/*

deploy_test:
	rm -r dist/
	rm -r audl.egg-info/
	python3 -m build
	python3 -m twine upload --repository testpypi dist/*
	# jupyter nbconvert --to notebook --inplace --execute examples/*.ipynb

precommit_hook:
	# cz init or python3 -m commitizen init
	pre-commit install
