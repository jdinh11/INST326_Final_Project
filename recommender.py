import sys
import re
import pandas as pd
from argparse import ArgumentParser


class Database():
    """A class for storing a dataframe of the dataset.

    Attributes:
        movies (DataFrame): the Neflix data.
    """
    def __init__(self, filepath):
        """Initializes a Database class.

        Args: 
            filepath (str): the filepath to the dataset.
        """
        self.movies = self.load_movie_data(filepath)
        self.movies = self.clean_data(self.movies)

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
        movie_df = pd.read_csv(filepath, index_col = "id", usecols=cols)
        
        return movie_df

    def clean_data(self, df):
        """Process the data and get rid/modify potential insuffiencient rows within the dataframe.

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

    def load_movies(self):
        """Create a list of Movie objects from the movie DataFrame.

        Return:
            movie_list (list): the list of Movie objects.
        """
        movie_list = []
        for index, row in self.movies.iterrows():
            movie_id = index
            title = row['title']
            media_type = row['type']
            movie_desc = row['description']
            genre = row['genres']
            age_rating = row['age_certification']
            imdb_score = row['imdb_score']
            movie = Movie(movie_id, title, media_type, movie_desc, genre, age_rating, imdb_score)
            movie_list.append(movie)
        
        return movie_list

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
            match = [m for m in database if m.title.lower() == movie.lower()]
            if not match:
                raise ValueError(f"{movie} does not exist within the database.")
            else:
                self.preferences.append(match)

class Recommender():
    """The main recommendation engine of the system
    
    """
    def __init__():
        pass

    def get_similar_movies(self, title):
        """Get recommendations based on friend's favorite movies

        Args: 
            title (str): the name of a movie
        """
        pass

    def format_results(self, recommendations):
        """Format the recommendation list for the user
        Args:
            recommedations (list): the list recommended movies
        
        Return:
            the recommendation displayed in the formatted structure
        """
        pass

def main(filepath):
    """Starts the recommender system

    Args: 
        filepath (str): the path to the csv file
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
                    break
                except ValueError as e:
                    print(e)
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