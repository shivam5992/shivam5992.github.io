import requests 
import ast 
from BeautifulSoup import BeautifulSoup
import htmlmin

import os 

def get_data():
	url = 'http://www.shivambansal.com'
	resp = requests.get(url)
	html = resp.text
	soup = BeautifulSoup(html)

	fout = open('blogs.txt', 'w')
	for li in soup.findAll('div' , {'class' : 'post-preview'}):
		post = {}
		post['url'] = li.a['href']
		post['title'] = li.h2.text
		post['desc'] = li.h3.text
		post['date'] = li.p.text.replace("Posted on", "") 
		
		resp = requests.get("http://www.shivambansal.com/" + post['url'])
		html = resp.text
		soup = BeautifulSoup(html)
		txt = soup.find('div' , {'class' : 'col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1 arttext'})
		post['text'] = txt
		print post['url']
		fout.write(str(post) + "\n")

def generate_html(post):

	txt = str([post['text']])
	txt = txt.replace("""['<div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1 arttext">""","""""")
	txt = txt.replace("""<br /']""","""""")
	if txt.endswith("']"):
		txt = txt.replace("""']""", "")
	if txt.startswith("['"):
		txt = txt.replace("['","")

	txt = txt.replace("!!!!-","\n")
	txt = txt.replace("!!!!","\n\t")
	# print txt 
	# exit(0)

	html = """<!DOCTYPE html>
		<html lang="en"><html>
		<head>
			<meta charset="utf-8" />
			<meta http-equiv="X-UA-Compatible" content="IE=edge" />
			<title>""" + post['title'] + """ - Shivam Bansal's Blog</title>
			<meta name="description" content="" />
			<meta name="HandheldFriendly" content="True" />
			<meta name="viewport" content="width=device-width, initial-scale=1.0" />
			<link rel="shortcut icon" href="../../img/SB.png">
			<link rel="canonical" href="http://shivambansal.com/""" + post['url'] + """" />
			<meta name="referrer" content="origin" />
			<meta property="og:site_name" content="Shivam Bansal" />
			<meta property="og:type" content="article" />
			<meta property="og:title" content='""" + post['title'] + """' />
			<meta property="og:description" content='""" + post['desc'] + """' />
			<meta property="og:url" content='http://shivambansal.com/""" + post['url'] + """' />
			<meta property="og:image" content="../../img/post-bg.jpg" />
			<meta property="article:published_time" content='""" + post['date'] + """' />
			<meta property="article:tag" content="" />
			<meta property="article:tag" content="" />
			<link href="../../css/bootstrap.min.css" rel="stylesheet">
			<link href="../../css/clean-blog.css" rel="stylesheet">
			<link href='http://fonts.googleapis.com/css?family=Open+Sans:300,400' rel='stylesheet' type='text/css'>
		</head>

		<body>
			<nav class="navbar navbar-default navbar-custom navbar-fixed-top">
				<div class="container-fluid">
					<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
						<ul class="nav navbar-nav navbar-right">
							<li>
								<a href="../../index.html">Home</a>
							</li>
							<li>
								<a href="../../about/">About</a>
							</li>

						</ul>
					</div>
				</div>
			</nav>

			<header class="intro-header" style="background-image: url('../../img/post-bg.jpg')">
				<div class="container sam">
					<div class="row">
						<div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
							<div class="post-heading">
								<h1>""" + post['title'] + """</h1>
								<span class="sub-desc">Posted on """ + post['date'] + """</span>
							</div>
						</div>
					</div>
				</div>
			</header>

			<article>
				<div class="container">
					<div class="row">
						<div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1 arttext">
							""" + txt + """

							<br>
		                    <div id="disqus_thread"></div>
		                    <script type="text/javascript">
		                    /* * * CONFIGURATION VARIABLES * * */
		                    var disqus_shortname = 'shivambansal';

		                    /* * * DON'T EDIT BELOW THIS LINE * * */
		                    (function() {
		                        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
		                        dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
		                        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
		                    })();
		                    </script>

						</div>
					</div>
				</div>
			</article>

			<hr>
			<footer>
				<div class="container">
					<div class="row">
						<div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
							<p class="copyright text-muted">&copy; shivambansal.com 2016</p>
						</div>
					</div>
				</div>
			</footer>

			<script>
			(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
				(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
				m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
			})(window,document,'script','//www.google-analytics.com/analytics.js','ga');
			ga('create', 'UA-45186276-1', 'shivambansal.com');
			ga('send', 'pageview');
			</script>
		</body>
		</html>"""

	if not os.path.exists(post['url']):
		os.mkdir(post['url'])	
	fout = open(post['url'] + 'index.html', 'w')
	fout.write(html.encode('utf8'))
	
	return

def generate_all_posts():
	data = open('blog/jsons/blogs.txt').read().strip().split("\n")
	for line in data:
		post = ast.literal_eval(line)
		generate_html(post)		

def generate_index():
	data = open('blog/jsons/blogs.txt').read().strip().split("\n")
	tagged = ""
	for line in data:
		post = ast.literal_eval(line)

		if not "<div" in post['desc']:
			post['desc'] = post['desc'][:200]

		post_content = """  <div class="post-preview">
                    		<a href='""" + post['url'] + """'>
                        		<h2 class="post-title">""" + post['title'] + """</h2>
                        	</a>
                        		<p class="post-subtitle">""" + post['desc'] + """</p>
                    		<p class="post-meta">""" + post['date'] + """</p>
                			</div><hr>"""
		tagged += post_content
		
	index = """<!DOCTYPE html>
			<html lang="en">
			<head>
			    <meta charset="utf-8" />
			    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
			    <title>Shivam Bansal - Home</title>
			    <meta name="description" content="Shivam Bansal is a Data Scientist, who likes to solve real world data problems using
			    Natural Language Processing and Machine Learning. He is focussed towards building full stack solutions and architectures." />
			    <meta name="HandheldFriendly" content="True" />
			    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
			    <meta property="og:locale" content="en_US">
			    <meta property="og:type" content="article">
			    <meta property="og:site_name" content="Shivam Bansal">
			    <meta property="og:url" content="http://shivambansal.com">
			    <meta name="og:title" content="Shivam Bansal">
			    <meta name="og:description" content="Shivam Bansal is a Data Scientist, who likes to solve real world data problems using
			    Natural Language Processing and Machine Learning. He is focussed towards building full stack solutions and architectures.">
			    <meta name="og:image" content="img/home-bg.jpg">

			    <link rel="canonical" href="http://shivambansal.com" />
			    <link rel="shortcut icon" href="img/SB.png">
			    <meta name="referrer" content="origin" />
			    <meta property="og:site_name" content="Shivam Bansal" />
			    <meta property="og:type" content="website" />
			    <meta property="og:title" content="Shivam Bansal" />
			    <meta property="og:description" content="Shivam Bansal is a Data Scientist, who likes to solve real world data problems using
			    Natural Language Processing and Machine Learning. He is focussed towards building full stack solutions and architectures." />
			    <meta property="og:url" content="http://shivambansal.com" />
			    <meta property="og:image" content="img/home-bg.jpg" />
			    </script>

			    <link href="css/bootstrap.min.css" rel="stylesheet">
			    <link href="css/clean-blog.css" rel="stylesheet">
			    <link href='http://fonts.googleapis.com/css?family=Open+Sans:300,400' rel='stylesheet' type='text/css'>
			</head>

			<body>
		    <header class="intro-header" style="background-image: url('img/home-bg.jpg')">
		        <div class="container">
		            <div class="row">
		                <div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
		                    <div class="site-heading">
		                        <h1>Shivam Bansal</h1>
		                    	<p class="sub-desc">The guy who loves to create world class algorithms and solutions for real world data problems
		                    	<br>
		                    	Data Scientist &bull; Machine Learning &bull; NLP &bull; Big Data &bull; Full Stack</p>
		                    	<a href="about/" class="btn btn-default sub-btn">About Me</a>
		                    </div>
		                </div>
		            </div>
		        </div>
		    </header>

		    <div class="container">
		        <div class="row">
		            <div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
		            	""" + tagged + """
		            </div>
		        </div>
		    </div>

			<footer>
			    <div class="container">
			        <div class="row">
			            <div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
			                <p class="copyright text-muted"> &copy; Shivam Bansal 2016</p>
			            </div>
			        </div>
			    </div>
			</footer>	
		    <script>
		        (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
		        (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
		        m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
		        })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
		        ga('create', 'UA-45186276-1', 'shivambansal.com');
		        ga('send', 'pageview');
		    </script>
			</body>
			</html>"""


	fout = open('index.html', 'w')
	soup = BeautifulSoup(index.encode('utf8'))
	prettified = soup.prettify(encoding="utf8")
	fout.write(prettified)

	return 

generate_all_posts() # NN , Voice
# generate_index()
post = {
	'text' : """<p>Data Mining is the technique of creating a raw data set by capturing data from a data source. The term data mining though has a broader meaning when talked about analytics, but in this blog we will discuss about data mining as the first and initial step of any data science application which deals primarily with data collection and data extraction ... <br><br> Read the complete article on mUniversity Blog official website, <a href="http://muniversity.mobi/blog/getting-started-with-data-science-data-mining/" target="_blank">Here</a> <br /><a href="http://muniversity.mobi/blog/getting-started-with-data-science-data-mining/" target="_blank"><div class="img-post"><img src="http://muniversity.mobi/blog/wp-content/uploads/2015/12/798x398xprocess1-798x398.jpg.pagespeed.ic._ilshEFseU.jpg" /></div></a></p>""",
	'title' : 'Getting Started with Data Science - Data Mining',
	'date' : 'Dec 10, 2015',
	'desc' : 'Data Mining is a process of collecting data, extraction of data and preparation of raw data set. It results in formation of a datasets which are in the ready to analyse formats.',
	'url' : 'blog/data-mining/'
}
generate_html(post)