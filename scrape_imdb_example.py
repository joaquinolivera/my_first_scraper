from request import get
from bs4 import BeautifulSoup
import pandas as pd
import csv
import sys


titles = []
years=[]
durations = []
genres = []
ratings = []
votes = []
grosses = []

max_number_of_items = 50

def imdb_page_scrape(number_of_page):
	url = 'https://www.imdb.com/search/title/?groups=top_1000&start={}&ref_=adv_prv'.format(number_of_page)
	response = requests.get(url, headers={'User-Agent':'Chrome/35.0.1916.47'})
	html = response.content

	soup = BeautifulSoup(html, "html.parser")


	def set_data_of_movies(movie):
		titles.append(movie.h3.a.text)
		years.append(movie.h3.find('span', class_='lister-item-year').text)
		durations.append(movie.p.find('span',class_='runtime').text)
		genres.append(movie.p.find('span',class_='genre').text)
		ratings.append(movie.strong.text)
		nv = movie.findAll('span', attrs={'name': 'nv'})
		votes.append(nv[0].text)
		if len(nv) > 1:
			grosses.append(nv[1].text)
		else:
			grosses.append('Not found')


	list_of_movies = soup.find_all('div',class_='lister-item mode-advanced')
	for movie in list_of_movies:
		set_data_of_movies(movie)
	

for i in range(21):
	imdb_page_scrape(i*max_number_of_items)

movies = pd.DataFrame({
	'movie_name': titles,
	'year':years,
	'time_in_min':durations,
	'genres':genres,
	'rating':ratings,
	'votes':votes,
	'grosses':grosses,
})

movies['year'] = movies['year'].str.extract('(\d+)').astype(int)

movies.to_csv('imdb_movies.csv')
