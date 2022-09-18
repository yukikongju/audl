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

pip: 
	rm -r dist/
	rm -r audl.egg-info/ 
	python3 -m build 
	jupyter nbconvert --to notebook --inplace --execute examples/*.ipynb
