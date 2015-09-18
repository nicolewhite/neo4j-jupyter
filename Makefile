slides:
	jupyter nbconvert main.ipynb --to slides --post serve

html:
	jupyter nbconvert main.ipynb
	open main.html
