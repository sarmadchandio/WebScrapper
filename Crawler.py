from bs4 import BeautifulSoup
import sys
import requests


def crawler(new_page, pages_visited, name):

	""" A function which extracts all the decendants of tag <a and searches for links sublinks of the same
		website in href. Includes all the subdomains of the website too. Downloads the html content of each
		website and store it in separate files."""


	url = requests.get(new_page)
	page_html = url.text

	# Converts the html into python objects
	soup = BeautifulSoup (page_html, 'html5lib')
	print (new_page + " <--- " , len(pages_visited))

	# Write the contents of current page into a seperate file
	# file = soup.title.string + str(len(pages_visited)) + '.html'
	file = str(len(pages_visited)) + '.html'
	print("File: ", file)
	with open(file, 'wb') as outfile:
		outfile.write(url.content)

	# A loop to that scrapes through all the links of the current page
	for link in soup.find_all('a'):
		if link.has_attr('href'):
			currentpage = link.get('href')
			#Searches if the domain the any unsearched page
			if ('http' not in currentpage) and ('www.' not in currentpage) and ('mailto' not in currentpage) and ('javascript' not in currentpage) and ('pdf' not in currentpage) and (domain+link.get('href') not in pages_visited):
				pages_visited.append(str(new_page+link['href']))
				crawler (new_page+link['href'], pages_visited, name)
			#Searches for sub-domains like forum. etc.
			elif name in currentpage and currentpage not in pages_visited:
				pages_visited.append(str(currentpage))
				crawler (currentpage, pages_visited, name)

			


def main():

	domain = "http://www.example.com/"

	# Extracts the name of the website "excluding htttp://" to find the sub-domains
	if 'https' in domain:
		name = domain[8:]
	elif 'http'in domain:
		name = domain[7:]
	print (name)
	pages_visited = [domain]


	url = requests.get(domain)
	page_html = url.text

	# Converts the html into python objects
	soup = BeautifulSoup (page_html, 'html5lib')


	crawler(domain,pages_visited, name)

if __name__ == "__main__":
	main()





