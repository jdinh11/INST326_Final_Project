import sys
import re
import pandas as pd
from argparse import ArgumentParser


class Database():
    """A class for storing a dataframe of the dataset.

    Attributes:
        movies (DataFrame): dataframe containing the Neflix data.
    """
    def __init__(self, filepath):
        """Initializes a Database class.

        Args: 
            filepath (str): the filepath to the dataset.
        """
        movies = self.load_movie_data(filepath)
        movies = self.clean_data(self.movies)
        self.movies = movies

    def load_movie_data(self, filepath):
        """Create a Pandas DataFrame using the CSV file containing Netflix shows and movies.

        Args:
            filepath (str): the filepath to the dataset.

        Return:
            the movies data as a Pandas DataFrame.
        """
        #identify the columns to include in the dataframe
        cols = ["id", "title", "type", "description", "age_certification", "genres", "imdb_score"]
        #load move data from the CSV using Pandas
        movie_df = pd.read_csv(filepath, usecols=cols)
        
        return movie_df

    def clean_data(self, df):
        """Process the data and get rid of/modify potential insuffiencient rows within the dataframe.

        Args:
            datas (tuple): rows of data for processing.

        Return:
            the polished rows of data.
        """
        #remove movies without a genres from the movie DataFrame
        df = df[(df['genres'] != '[]') | df['title'].notnull()]
        
        # Keep only the first occurrence of each duplicated value
        df.drop_duplicates(subset=['title'], keep='first', inplace=True)

        # Remove movie or show names that contain character that are not ASCII
        pattern = r'[^\x00-\x7F]+'
        non_english = df['title'].str.contains(pattern)
        df = df[~non_english]
        
        return df
    
class Movie():
    """A class for storing information regarding a list of Netflix medias.

    Attributes:
        movie_id (str): the media's id.
        title (str): the media's title.
        media_type (str): the type of media (movie or show).
        genre (list): the media's list of associated gernes.
        age_ratings (str): the media's age restrictions (if any).
        imdb_score (int): the media's imdb ratings.
    """
    def __init__(self, movie_id, title, media_type, movie_desc, genre, age_rating, imdb_score):
        """Initializes a Movie class.

        Args:
            movie_id (str): see class documentation.
            title (str): see class documentation.
            media_type (str): see class documentation.
            genre (list): see class documentation.
            age_rating (str): see class documentation.
            imdb_score (float): see class documentation.
        """
        self.movie_id = movie_id
        self.title = title
        self.media_type = media_type
        self.movie_desc = movie_desc
        self.genre = genre
        self.age_rating = age_rating
        self.imdb_score = imdb_score

    def __str__(self):
        """Returns a string representation of the Movie object.

        Return:
            str: a string representation of the Movie object detailings the movie's attributes.
        """
        return f"""\
            Name: {self.title}
            ID: {self.movie_id}
            Media Type: {self.media_type}
            Description: {self.movie_desc}
            Genre: {self.genre}
            Age Certification: {self.age_rating}
            IMDB Score: {self.imdb_score}
            """

class User():
    """Stores information regarding each users' preferences.
    
    Attributes:
        name (str): the user's name.
        preferences (list): a list of Movie objects pertaining to a user's favorite shows/movies.
    """
    def __init__(self, name):
        """Initializes a User object

        Args:
            name (str): see class documentation
        """
        self.name = name
        self.preferences = []
    
    def add_preference(self, movie, database):
        if movie.lower() not in [m.title.lower() for m in self.preferences]:
            match = database.movies[database.movies['title'].str.contains(movie, case = False)]
            if match.any():
                index = match.idxmax()
                result = database.movies.loc[index]

                movie_id = result[0]
                title = result[1]
                media_type = result[2]
                desc = result[3]
                age_restriction = result[4]
                genre = result[5]
                imdb_score = result[6]
                
                media = Movie(movie_id, title, media_type, desc, age_restriction, genre, imdb_score)
                self.preferences.append(media)
            
            else:
                raise ValueError(f"Media with name \"{movie}\" does not exist within the database.")

class Recommender():
    """The main recommendation engine of the system
    
    Attributes:
        common_genres (dict): A dictionary containing the common favorite genres between the user and one of their friends
    """
    def __init__(self, user, friend):
        """Initializes a Recommender class. Sort the dictionary of common genre between two people.
        
        Args: 
            user (User): the User object containing info about the user and their preferences.
            friend (User): the User object containing info about the user's chosen friend and their preferences.
        """
        common_genres = self.get_common_genres(user, friend)
        sorted_common_genres = {}

        for key, value in sorted(common_genres.items(), key = lambda x: x[1]): 
            sorted_common_genres[key] = value

        self.common_genres = sorted_common_genres

    def get_common_genres(self, user, friend):
        """Searches and ranks the shared genre between two users based on number of match occurances.

        Args: 
            user (User): the User object containing info about the user and their preferences.
            friend (User): the User object containing info about the user's chosen friend and their preferences.

        Return:
            dict: a dictionary where the key is the shared genre between two users and the amount of matches found for each shared genres.
        """
        user_genres = {}
        friend_genres = {}

        for u in user.preferences:
            for genre in u.genre:
                if genre in user_genres.keys():
                    user_genres[genre] += 1
                else:
                    user_genres[genre] = 1
        
        for f in friend.preferences:
            for genre in f.genre:
                if genre not in friend_genres.keys():
                    friend_genres[genre] += 1
                else:
                    friend_genres[genre] = 1
        
        shared_genres = user_genres.keys() & friend_genres.keys()
        common_genres = {genre: user_genres[genre] + friend_genres[genre] for genre in shared_genres}

        
        return common_genres

    def get_recommendation(self, database):
        """Get movies/shows recommendation based on the common genres of the user and their friend.

        Args:
            shared_genres (list): a dictionary of common genres between the user and their friend.
        
        Return:
            DataFrame: the recommended movies/shows.
        """
        search_genres = self.common_genres.keys()
        
        database.movies['num_matches'] = database.movies['genres'].apply(lambda x: x.isin(search_genres).sum())
        df = database.movies.sort_value(by = 'num_matches', ascending = False)
        
    def sort_by_score(self, df):
        """Sort the recommendations narrowed down by genre by IMDb scores (descending order).
        
        Args:
            df (dataframe): a dataframe containing a sorted list of recommendations based on shared genres
            
        Return:
            score_df (dataframe): recommendations sorted by IMDb scores. 
        """
        score_df = df.sort_value(by = 'imdb_score', ascending = False)
        return score_df

def main(filepath):
    """Starts the recommender system.

    Args: 
        filepath (str): the path to the csv file.
    """
    database = Database(filepath)
    user_list = []
    while True:
        name = input("Give me the name of a user: ")
        user = User(name)
        user_list.append(user)
        while True:
            while True:
                try:
                    movie = input("Enter a movie name to add it to this user's preference list: ")
                    user.add_preference(movie, database)
                except ValueError as e:
                    print(e)
                break
            add_movie = input("Would you like to add another movie? Type \"yes\" or \"no\": ")
            if add_movie == 'no':
                break
        
        add_user = input("Would you like to add another user? Type \"yes\" or \"no\": ")
        if add_user == 'no':
            break

def parse_args(arglist):
    """Takes a list of strings from the command prompt and passes them through as arguments
    
    Args:
        args_list (list) : the list of strings from the command prompt
    
    Returns:
        args (ArgumentParser)
    """
    parser = ArgumentParser()
    parser.add_argument("filepath", type=str, help="path to the CSV file with data about Netflix TV Shows and Movies")

    return parser.parse_args(arglist)

if __name__ == "__main__":
    arguments = parse_args(sys.argv[1:])
    main(arguments.filepath)