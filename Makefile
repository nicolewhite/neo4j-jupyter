slides:
	jupyter nbconvert basics.ipynb --to slides --post serve

html:
	jupyter nbconvert basics.ipynb
	open basics.html
