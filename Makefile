slides:
	jupyter nbconvert hello-world.ipynb twitter.ipynb --to slides && python -m SimpleHTTPServer
	
html:
	jupyter nbconvert main.ipynb hello-world.ipynb twitter.ipynb
	open main.html
