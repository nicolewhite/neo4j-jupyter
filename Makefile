slides:
	jupyter nbconvert hello-world.ipynb twitter.ipynb --to slides
	mv hello-world.slides.html build
	mv twitter.slides.html build
	
html:
	jupyter nbconvert index.ipynb hello-world.ipynb twitter.ipynb
	mv index.html build
	mv hello-world.html build
	mv twitter.html build
