slides:
	jupyter nbconvert hello-world.ipynb twitter.ipynb --to slides --post serve
	
html:
	jupyter nbconvert *.ipynb
	mv *.html build
