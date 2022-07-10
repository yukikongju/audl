.PHONY: docs
docs:	
	rm -r docs/ 
	pdoc --html audl 
	mv html/ docs/

clean:
	rm -r dist/
	rm -r audl.egg-info/ 

pip: 
	rm -r dist/
	rm -r audl.egg-info/ 
	python3 -m build 
