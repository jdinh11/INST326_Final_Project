import pytest
import pandas as pd
from recommender import Database, Movie, User

def test_Database():
    '''Tests the __init__ of the Database class and check if it intializes it.
    '''
    filepath = Database("titles.csv")
    #checks if the movies attribute of the filepath is initialized correctly as a Pandas Dataframe
    assert isinstance(filepath.movies, pd.DataFrame)
    #Checks that there is data in the DataFrame from the CSV file
    assert len(filepath.movies)

def test_load_movie_data():
    '''Tests to see if it creates a pandas dataframe using the csv file with the correct columns.
    '''
    filepath = "titles.csv"
    movie_df = Database(filepath)
    #checks if a movie_df instance was created successfully from the pandas dataframe
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
    '''Tests to see if the method cleans the dataframe correctly.
    '''
    movie_df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'title': ['title1', 'title2', 'title3', 'title1', 'PokÃ©mon'], #should remove the duplicate 'title1'(id:4) and 'PokÃ©mon' (id:5)
        'type': ['MOVIE1', 'MOVIE2', 'MOVIE3', 'MOVIE4', 'MOVIE5'], 
        'description': ['desc1', 'desc2', 'desc3', 'desc4', 'desc5'],
        'age_certification': ['age1', 'age2', 'age3', 'age4', 'age5'],
        'genres': ["['genre1']", "['genre2']" , None, "['genre4']", "['genre5']"], #should remove the column with empty genre (id:3)
        'imdb_score': [8.9, None, 7.9, 9.0, 8.7] #should replace any None value with a 0 in the imdb_score column (id:2)
    })
    
    #creates instance of Database using the filepath
    df = Database(filepath='titles.csv')
    #checks if the clean_data method works on the instance of Database
    movie_df_cleaned = df.clean_data(movie_df)
    #checks if all null values in 'imdb_score' column are replaced with 0 from the dataframe
    assert movie_df_cleaned['imdb_score'].isnull().sum() == 0
    #checks if movies without a genre are removed. Should be 2 while factoring the removed movies from id: 3,4,5.
    assert len(movie_df_cleaned.dropna(subset=['genres'])) == 2
    #checks if duplicated movie titles are removed
    assert len(movie_df_cleaned['title']) == len(movie_df_cleaned['title'].unique())
    #checks that movie names that are not ASCII chracters are removed 
    assert not movie_df_cleaned['title'].str.contains(r'[^\x00-\x7F]+').any()
    

def test_find_movie():
    '''Check if find_movie() functions as expected'''
    database = Database('titles.csv')

    result = database.find_movie('Arcane')
    assert result.movie_id == 'ts222333'
    assert result.title == 'Arcane'
    assert result.media_type == 'SHOW'
    assert result.movie_desc == 'Amid the stark discord of twin cities Piltover and Zaun, two sisters fight on rival sides of a war between magic technologies and clashing convictions.'
    assert result.age_rating == 'TV-14'
    assert result.genre == ['scifi', 'action', 'drama', 'animation', 'fantasy']
    assert result.imdb_score == 9.0

    result = database.find_movie('sdfoinef')
    assert result is None

def test_Movie():
    '''Tests the __init__ of the Movie class and if it intializes it.
    '''
    movie_id = "tm69997"
    title = "Richard Pryor: Live in Concert"
    media_type = "MOVIE"
    movie_desc = "Richard Pryor delivers monologues on race, sex, family and his favorite target—himself, live at the Terrace Theatre in Long Beach, California."
    genre = "['comedy', 'documentation']"
    age_rating = "R"
    imdb_score = 8.1
    
    #creates movie object
    movie_obj = Movie(movie_id, title, media_type, movie_desc, genre, age_rating, imdb_score)
    #checks if the attributes of the object from the Movie class match the variables defined
    assert movie_obj.movie_id == "tm69997"
    assert movie_obj.title == "Richard Pryor: Live in Concert"
    assert movie_obj.media_type == "MOVIE"
    assert movie_obj.movie_desc == "Richard Pryor delivers monologues on race, sex, family and his favorite target—himself, live at the Terrace Theatre in Long Beach, California."
    assert movie_obj.genre == ['comedy','documentation']
    assert movie_obj.age_rating == "R"
    assert movie_obj.imdb_score == 8.1

def test_str():
    '''Tests if the string representation of the Movie object return correctly.
    '''
    movie_id = "tm69997"
    title = "Richard Pryor: Live in Concert"
    media_type = "MOVIE"
    movie_desc = "Richard Pryor delivers monologues on race, sex, family and his favorite target—himself, live at the Terrace Theatre in Long Beach, California."
    genre = "['comedy', 'documentation']"
    age_rating = "R"
    imdb_score = 8.1
    
    #creates movie object
    movie_obj = Movie(movie_id, title, media_type, movie_desc, genre, age_rating, imdb_score)
    #turns each attribute in the Movie object into a string
    str_title = str(movie_obj.title)
    str_movie_id = str(movie_obj.movie_id)
    str_media_type = str(movie_obj.media_type)
    str_movie_desc = str(movie_obj.movie_desc)
    str_genre = str(movie_obj.genre)
    str_age_rating = str(movie_obj.age_rating)
    str_imdb_score = str(movie_obj.imdb_score)
    #checks to see if the values in the attribute are all strings
    assert str_movie_id == "tm69997"
    assert str_title == "Richard Pryor: Live in Concert"
    assert str_media_type == "MOVIE"
    assert str_movie_desc == "Richard Pryor delivers monologues on race, sex, family and his favorite target—himself, live at the Terrace Theatre in Long Beach, California."
    assert str_genre == "['comedy', 'documentation']"
    assert str_age_rating == "R"
    assert str_imdb_score == "8.1"
    
def test_User():
    '''Tests if the User object initializes correctly.
    '''
    name = 'Megan'    
    #creates User object
    user_obj = User(name)
    #turns the name attribute in the User object into a string
    str_name = str(user_obj.name)
    #checks to see if the value in the attribute matches
    assert str_name == 'Megan'