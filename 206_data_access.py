###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import unittest 
import tweepy 
import requests 
import json 
import twitter_info
import sqlite3
from pprint import pprint 
# Begin filling in instructions....

#-------------------------------OMDB Data----------------------------------------------

OMDB_FNAME = "OMDB_cache.json"

try: 
	omdb_cache_file = open(OMDB_FNAME, 'r')
	omdb_cache_contents = cache_file.read()
	omdb_cache_file.close()
	omdb_CACHE_DICTION = json.loads(omdb_cache_contents)
except: 
	omdb_CACHE_DICTION = {}

movies = []

movie1 = input("Insert the movie that you want to search for and hit enter ")
movie2 = input("Insert the movie that you want to search for and hit enter ")
movie3 = input("Insert the movie that you want to search for and hit enter ")
movie_search_terms = [movie1, movie2, movie3] #list of the movies that the user imputed 

def omdb_api_call_and_cache(movie):
	omdb_baseurl = 'http://www.omdbapi.com/?'
	omdb_fullurl = requests.get(omdb_baseurl, params = {'t': movie})

	if movie in omdb_CACHE_DICTION: 
		omdb_text = omdb_CACHE_DICTION[movie]
	else: 
		omdb_CACHE_DICTION[movie] = omdb_fullurl.text 
		omdb_text = omdb_fullurl.text 

		omdb_cache_file = open(OMDB_FNAME, 'w')
		omdb_cache_file.write(json.dumps(omdb_CACHE_DICTION))
		omdb_cache_file.close()

	return(json.loads(omdb_text))

movie_1 = omdb_api_call_and_cache(movie_search_terms[0]) #invocation of omdb api and caching data
movie_2 = omdb_api_call_and_cache(movie_search_terms[1])
movie_3 = omdb_api_call_and_cache(movie_search_terms[2]) 

movie_dics = [movie_1, movie_2, movie_3] #list of movie dictionaries based of user search terms	


class Movie(): 
	def __init__(self, omdb_dic): 
		self.omdb_dic = omdb_dic
		self.imdb_rating = float(self.omdb_dic['imdbRating'])
		self.director = self.omdb_dic['Director'] 
		self.rated = self.omdb_dic['Rated']


	def get_all_actors(self): 
		actors = self.omdb_dic['Actors']
		actor_lst = actors.split(',')
		return actor_lst

	def get_lead_actor(self): 
		actor_lst = self.get_all_actors()
		lead_actor = actor_lst[0]
		return lead_actor	

	def get_title(self):
		return self.omdb_dic['Title']

	def get_release_date(self):
		return self.omdb_dic['Released']	 

	def get_num_lang(self): 
		lang_str = self.omdb_dic['Language']
		lang_lst = lang_str.split(',')	
		return len(lang_lst)

	def get_imdb_id(self):
		return self.omdb_dic['imdbID']	

	def __str__(self):
		title = self.get_title()
		director = self.director
		actor = self.get_lead_actor()
		rating = self.imdb_rating
		result = 'The name of the movie is: {} \n The director of the movie is: {} \n The leading actor is: {} \n The IMDB rating is: {}'.format(title, director, actor, rating)
		return result
			


movie_obj_lst = [] #list of movie objects using the dictionaries in movie_dics as input
for movie in movie_dics: 
	movie_object = Movie(movie)
	movie_obj_lst.append(movie_object) 
	

def get_movie_data(movie_lst): #this method gets a list of tuples of the 3 different movies searched for
	movie_data_tup_lst = []
	for movie in movie_obj_lst:  
		movie_id = movie.get_imdb_id()
		movie_director = movie.director
		movie_title = movie.get_title()
		movie_imdb_rating = movie.imdb_rating 
		movie_lead_actor = movie.get_lead_actor()
		movie_num_lang = movie.get_num_lang()

		movie_tup = (movie_id, movie_director, movie_title, movie_imdb_rating, movie_lead_actor, movie_num_lang)
		movie_data_tup_lst.append(movie_tup)

	return movie_data_tup_lst 

all_movie_data_tup = get_movie_data(movie_obj_lst) #This list of tuples contains various different attributes about the 3 movies searched for

pprint (all_movie_data_tup)


#-------------------------------SQL---------------------------------------------------


conn = sqlite3.connect('data_access.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Movies') 

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Movies (movie_id TEXT PRIMARY KEY, '
table_spec += 'director TEXT, title TEXT, imdb_rating INTEGER, lead_actor TEXT, num_languages INTEGER)'
cur.execute(table_spec)


statement = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?)'

for a in all_movie_data_tup: 
	cur.execute(statement, a)
conn.commit()	


# Put your tests here, with any edits you now need from when you turned them in with your project plan.


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)