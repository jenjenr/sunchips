"""Scrape SFUSD school information page for features of a school."""

import ast
from bs4 import BeautifulSoup
import cStringIO
import requests
import simplejson
import ssl
import urllib2


def get_school_info(url):
	"""Get information from school's SFUSD web page.
	Args:
		url: string of the url to school's SFUSD web page.
	Returns:
		dictionary of fields of interests to the text about them.
	"""
	# "http://www.sfusd.edu/en/schools/school-information/mckinley.html"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	content_children = list(soup.find_all(id='content-inner')[0].children)

	feature_name = ""
	school = {}
	for child in content_children:
		if child.name == 'h2':
			feature_name = child.get_text()
			continue
		# Extract subheading text from various elements
		feature_text = ""
		if child.name == 'p':
			feature_text = child.get_text().strip()
		elif child.name == 'ul':
			feature_text = extract_text_from_list(child)
		else:
			feature_text = str(child).strip()

		if feature_text:
			# If there was no heading for this data, it must
			# be data from the first few lines of the page.
			if not feature_name:
				extract_text_from_beginning(feature_text, school)
			elif feature_name in school:
				feature_text = ", " + feature_text
				school[feature_name].append(feature_text)
			else:
				school[feature_name] = [feature_text]
	return school

def extract_text_from_list(ul):
	text = ""
	for list_item in ul.children:
		if not text:
			text += list_item.get_text()
		else:
			text += ", "
			text += list_item.get_text()
	return text

def extract_text_from_beginning(paragraph_text, school):
	"""Beginning paragraphs have different formatting that is 
	separated by colons.
	Args:
		paragraph_text: string of the text in the element. Consists of
		a few lines, with feature name and feature text separated
		by a colon.
		school: dict of the feature names and texts for a school.
	"""
	lines = paragraph_text.split("\n")
	for line in lines:
		split_by_colon = line.split(': ')
		if len(split_by_colon) == 2:
			feature_name = split_by_colon[0].strip()
			feature_text = split_by_colon[1]
			school[feature_name] = feature_text
		# Special case for the address of the school
		else:
			if line.strip():
				school["Address"] = line.strip()

school = get_school_info("http://www.sfusd.edu/en/schools/school-information/balboa.html")

def get_great_schools_info(url, school):
	"""Get school reviews from GreatSchools.com.
	Args:
		url: link address for school's webpage on GreatSchools.com
		school: dict of the feature names and texts for a school. Adds
			reviews to this dict.

	"""
	page = requests.get(url, verify=False)
	soup = BeautifulSoup(page.content, 'html.parser')
	scripts = list(soup.find_all('script', {"data-component-name": 'Reviews'}))
	reviews = parse_review_text(scripts[0].get_text())
	school['reviews'] = reviews
	get_test_scores(soup, school)

def parse_review_text(text):
	split_by_commas = text.split(",")
	split_by_colons = []
	for segment in split_by_commas:
		split_by_colons.extend(segment.split(":"))
	reviews = []
	for i in range(len(split_by_colons)-1):
		if split_by_colons[i] == '{"comment"':
			reviews.append(split_by_colons[i+1])
	return reviews

def get_test_scores(soup, school):
	scores = list(soup.find_all(class_="score"))
	if len(scores) >= 4:
		school['English_test_score'] = scores[0].get_text()
		school['Math_test_score'] = scores[2].get_text()


get_great_schools_info("https://www.greatschools.org/california/san-francisco/6340-Balboa-High-School/", school)

