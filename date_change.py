import os 

for folder in os.listdir('blog'):
	try:
		fname = 'blog/' + folder + "/index.html"
		content = open(fname).read()

		content = content.replace("&copy; shivambansal.com 2016", "&copy; shivambansal.com 2017")
		
		outname = 'blog1/' + folder + "/index.html"
		os.makedirs('blog1/'+folder)
		fout = open(outname, 'w')
		fout.write(content)
	except Exception as E:
		print E 