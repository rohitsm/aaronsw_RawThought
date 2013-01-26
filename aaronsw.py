
import urllib2
import sys
from bs4 import BeautifulSoup
import time

#__author__ = Rohit Menon
#__Contact__ = rohitsm@gmail.com

link = "http://www.aaronsw.com/weblog/fullarchive"

def get_page_html(link):
	try:
		req = urllib2.Request(link.strip())
		file = urllib2.urlopen(req)
		page = file.read()
		file.close()
		return page
	except:
		print 'this is get_page'
		print sys.exc_value

data = get_page_html(link)
soup = BeautifulSoup(data)

def get_all_title_links(data):
	for row in soup.body.findAll(True, {"class":"content"}):
		links_list = [link['href'] for link in row.findChildren("a")]
		title_urls = []
		post_titles = []
		for i  in links_list:
			url = i.encode("utf8")
			post_titles.append(url)
			title_urls.append("http://www.aaronsw.com/weblog/%s"%url)
		return title_urls, post_titles

title_urls_list, post_titles = get_all_title_links(link)
print "No of total links: ", len(title_urls_list)
bad_urls = []

# Program can also be modified to read the URLs directly from 
# title_urls_list instead of reading from file "EntryLinks.txt"

def get_blog_post(title_urls_list, post_titles):
	# Keeps list of urls after reading from file
	array = [] 
	current_link = "http://www.aaronsw.com/weblog/tdk"
	f = open("RawThoughts.txt",'w')
	for url in open("EntryLinks.txt", "r").readlines():
		array.append(url.strip("\n"))
	
	flag_point = array.index(current_link)
	print "Flag Point", flag_point
	for i in range(flag_point, len(array)):
		url = array[i]
		m = array.index(url)
		print "Getting URL : ", url
		print "Post No: ", m
		
		try:
			page = get_page_html(str(url))
			soup = BeautifulSoup(page)
		except:
			print "HTTP 404 encountered and flagged - ", url
			bad_urls.append(url)
			print "Flagged m = ", m

		f.write( "\n====================================================\n")

		for p in soup.findAll("div",{"class": "content"}):
			date = [date.text for date in p.findAll(True, {"class":"posted"})]
			post_date = date[0]
			f.write("Date: " + (post_date).encode("ascii", "ignore")+"\n \n")
			for t in p.findAll("h1"):
				f.write("Title: " + (t.text).encode("ascii", "ignore")+"\n \n")
			for t in p.findAll("p"):
				f.write((t.text).encode("ascii", "ignore")+"\n \n")

		m = m+1
	f.close()

start_time = time.time()
get_blog_post(title_urls_list, post_titles)
end_time = time.time()-start_time
print "End of program: ", end_time
print "No of bad urls = ", len(bad_urls)
print "Bad urls", bad_urls



