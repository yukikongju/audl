.PHONY: docs
docs:
	rm -r docs/
	# pdoc --html audl
	uv run pdoc --html audl
	mv html/ docs/

clean:
	rm -r dist/
	rm -r audl.egg-info/

.PHONY: tests
tests:
	# python3 -m unittest tests/stats/endpoints/*
	uv run python -m unittest tests/stats/endpoints/*

deploy:
	# rm -r dist/
	# rm -r audl.egg-info/
	# python3 -m build
	uv build
	# twine upload dist/*
	# python3 -m twine upload dist/*
	uv run twine upload dist/*

deploy_test:
	# rm -r dist/
	# rm -r audl.egg-info/
	# python3 -m build
	uv build
	# python3 -m twine upload --repository testpypi dist/*
	uv run twine upload --repository testpypi dist/*
	# jupyter nbconvert --to notebook --inplace --execute examples/*.ipynb

precommit_hook:
	# pre-commit install
	uv run pre-commit install

commitizen_commit:
	# cz init or python3 -m commitizen init
	# cz commit
	# cz bump
	# python3 -m commitizen commit
	uv run python -m commitizen commit
