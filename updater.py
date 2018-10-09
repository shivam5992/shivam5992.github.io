import os 

files = os.listdir("blog/")

for file in files:
	if file.startswith("."):
		continue
	# txt = open("blog/" + file + "/index.html").read()
	# txt = txt.replace('<a href="../../about/">About</a>', '')
	# fout = open("blog/" + file + "/index_1.html", "w")
	# fout.write(txt)

	# os.rename("blog/" + file + "/index.html", "blog/" + file + "/index_old.html")

	# os.rename("blog/" + file + "/index_1.html", "blog/" + file + "/index.html")	

	## after this you can delete index_old.html