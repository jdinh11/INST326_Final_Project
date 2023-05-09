import pytest
import pandas as pd
from recommender import Database, Movie

def test_load_movie_data():
    
    filepath = "titles.csv"
    movie_df = Database(filepath)
    movies = movie_df.load_movie_data(filepath)
    assert 'id' in movies.columns
    assert 'title' in movies.columns
    assert 'type' in movies.columns
    assert 'description' in movies.columns
    assert 'age_certification' in movies.columns
    assert 'genres' in movies.columns
    assert 'imdb_score' in movies.columns

def test_movie():
    
    movie_obj = Movie("tm70993", "Life of Brian", "MOVIE", "Brian Cohen is an average young Jewish man, but through a series of ridiculous events, he gains a reputation as the Messiah. When he's not dodging his followers or being scolded by his shrill mother, the hapless Brian has to contend with the pompous Pontius Pilate and acronym-obsessed members of a separatist movement. Rife with Monty Python's signature absurdity, the tale finds Brian's life paralleling Biblical lore, albeit with many more laughs.", ['comedy','GB'], "R", 8.0)
    assert movie_obj.movie_id == "tm70993"
    assert movie_obj.title == "Life of Brian"
    assert movie_obj.media_type == "MOVIE"
    assert movie_obj.movie_desc == "Brian Cohen is an average young Jewish man, but through a series of ridiculous events, he gains a reputation as the Messiah. When he's not dodging his followers or being scolded by his shrill mother, the hapless Brian has to contend with the pompous Pontius Pilate and acronym-obsessed members of a separatist movement. Rife with Monty Python's signature absurdity, the tale finds Brian's life paralleling Biblical lore, albeit with many more laughs."
    assert movie_obj.genre == ['comedy','GB']
    assert movie_obj.age_rating == "R"
    assert movie_obj.imdb_score == 8.0
    
def test_movie_str():
    movie_obj = Movie("tm69997", "Richard Pryor: Live in Concert", "MOVIE", "Richard Pryor delivers monologues on race, sex, family and his favorite target—himself, live at the Terrace Theatre in Long Beach, California.", ['comedy', 'documentation'], "R", 8.1)
    
    str_movie_obj = str(movie_obj)
    
    assert "Name: Richard Pryor: Live in Concert" in str_movie_obj
    assert "ID: tm69997" in str_movie_obj
    assert "Media Type: MOVIE" in str_movie_obj
    assert "Description: Richard Pryor delivers monologues on race, sex, family and his favorite target—himself, live at the Terrace Theatre in Long Beach, California." in str_movie_obj 
    assert "Genre: ['comedy', 'documentation']" in str_movie_obj
    assert "Age Certification: R" in str_movie_obj
    assert "IMDB Score: 8.1" in str_movie_obj
    
    




