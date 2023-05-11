import pytest
import pandas as pd
from recommender import Database, Movie

def test_Database():
    filepath = Database("titles.csv")
    #checks if the movies attribute of the Database class is initialized correctly as a Pandas Dataframe
    assert isinstance(filepath.movies, pd.DataFrame)
    #Checks that there is data in the DataFrame from the CSV file
    assert len(filepath.movies)

def test_load_movie_data():
    filepath = "titles.csv"
    movie_df = Database(filepath)
    assert isinstance(movie_df.load_movie_data(filepath), pd.DataFrame)
    #checks if the columns have been created correctly in the DataFrame
    assert 'id' in movie_df.movies
    assert 'title' in movie_df.movies
    assert 'type' in movie_df.movies
    assert 'description' in movie_df.movies
    assert 'age_certification' in movie_df.movies
    assert 'genres' in movie_df.movies
    assert 'imdb_score' in movie_df.movies

def test_clean_data():
    movie_df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'title': ['title1', 'title2', 'title3', 'title1', 'PokÃ©mon'], #should remove the column with 'PokÃ©mon'(id:4) and duplicate 'title1'(id:5)
        'type': ['MOVIE1', 'MOVIE2', 'MOVIE3', 'MOVIE4', 'MOVIE5'], 
        'description': ['desc1', 'desc2', 'desc3', 'desc4', 'desc5'],
        'age_certification': ['age1', 'age2', 'age3', 'age4', 'age5'],
        'genres': ["['genre1', 'genre2']", "['genre1']" , None, "['genre1']", "['genre1']"], #should remove the column with empty genre (id:3)
        'imdb_score': [8.9, None, 7.9, 9.0, 8.7] #should remove the column with an empty imdb_score (id:2)
    })
    
    df = Database(filepath='titles.csv')
    #checks if the clean_data method works on the instance of Database
    movie_df_cleaned = df.clean_data(movie_df)
    #checks if all null values in 'imdb_score' column are replaced with 0 from the dataframe
    assert movie_df_cleaned['imdb_score'].isnull().sum() == 0
    #checks if movies without a genre or titles are removed. Should be 3.
    assert len(movie_df_cleaned) == 3
    #checks if duplicated movie titles are removed
    assert len(movie_df_cleaned['title']) == len(movie_df_cleaned['title'].unique())
    #checks that movie names that contain ASCII chracters are removed 
    assert not movie_df_cleaned['title'].str.contains(r'[^\x00-\x7F]+').any()
    
def test_Movie():
    movie_id = "tm70993"
    title = "Life of Brian"
    media_type = "MOVIE"
    movie_desc = "Brian Cohen is an average young Jewish man, but through a series of ridiculous events, he gains a reputation as the Messiah. When he's not dodging his followers or being scolded by his shrill mother, the hapless Brian has to contend with the pompous Pontius Pilate and acronym-obsessed members of a separatist movement. Rife with Monty Python's signature absurdity, the tale finds Brian's life paralleling Biblical lore, albeit with many more laughs."
    genre = "['comedy','GB']"
    age_rating = "R"
    imdb_score = 8.0
    #creates movie object
    movie_obj = Movie(movie_id, title, media_type, movie_desc, genre, age_rating, imdb_score)
    #checks if the attributes of the object from the Movie class match the varables defined
    assert movie_obj.movie_id == "tm70993"
    assert movie_obj.title == "Life of Brian"
    assert movie_obj.media_type == "MOVIE"
    assert movie_obj.movie_desc == "Brian Cohen is an average young Jewish man, but through a series of ridiculous events, he gains a reputation as the Messiah. When he's not dodging his followers or being scolded by his shrill mother, the hapless Brian has to contend with the pompous Pontius Pilate and acronym-obsessed members of a separatist movement. Rife with Monty Python's signature absurdity, the tale finds Brian's life paralleling Biblical lore, albeit with many more laughs."
    assert movie_obj.genre == ['comedy','GB']
    assert movie_obj.age_rating == "R"
    assert movie_obj.imdb_score == 8.0
    

    




