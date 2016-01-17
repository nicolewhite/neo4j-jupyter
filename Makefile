slides:
	jupyter nbconvert hello-world.ipynb twitter.ipynb --to slides --post serve
	
html:
	jupyter nbconvert index.ipynb hello-world.ipynb twitter.ipynb
	mv index.html build
	mv hello-world.html build
	mv twitter.html build
