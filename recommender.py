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
        self.movies = self.load_movie_data(filepath)
        self.movies = self.clean_data(self.movies)
        

    def load_movie_data(self, filepath):
        """Create a Pandas DataFrame using the CSV file containing Netflix shows and movies.

        Args:
            filepath (str): the filepath to the dataset.

        Return:
            DataFrame: the movies data as a Pandas DataFrame.
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
            DataFrame: the polished rows of data.
        """
        df_copy = df.copy()
        #fill in NaN values within imdb_score column with 0
        df_copy['imdb_score'].fillna(0, inplace = True)
        
        #remove movies without a genres from the movie DataFrame
        df_copy = df_copy[(df_copy['genres'] != '[]') | df['title'].notnull()]
        
        # Keep only the first occurrence of each duplicated value
        df_copy.drop_duplicates(subset=['title'], keep='first', inplace=True)

        # Remove movie or show names that contain character that are not ASCII
        pattern = r'[^\x00-\x7F]+'
        non_english = df_copy['title'].str.contains(pattern)
        df_copy = df_copy[~non_english]
        
        return df_copy
    
    def find_movie(self, movie):
        """Search for a specific movie within the database.

        Args:
            movie (str): the title of the movie.

        Return:
            a string if a movie was found, or None if the movie name is not in the database.
        """
        match = self.movies.loc[self.movies['title'].str.contains(movie, case = False)]
        if not match.empty:
            media = Movie(match['id'].iloc[0], match['title'].iloc[0], match['type'].iloc[0], match['description'].iloc[0], match['genres'].iloc[0], match['age_certification'].iloc[0], match['imdb_score'].iloc[0]) 
            return media
        else:
            return None
        
class Movie():
    """A class for storing information regarding a list of Netflix medias.

    Attributes:
        movie_id (str): the media's id.
        title (str): the media's title.
        media_type (str): the type of media (movie or show).
        movie_desc (str): the description of the media.
        genre (list): the media's list of associated gernes.
        age_ratings (str): the media's age restrictions (if any).
        imdb_score (float): the media's imdb ratings.
    """
    def __init__(self, movie_id, title, media_type, movie_desc, genre, age_rating, imdb_score):
        """Initializes a Movie class.

        Args:
            movie_id (str): see class documentation.
            title (str): see class documentation.
            media_type (str): see class documentation.
            movie_desc (str): see class documentation.
            genre (list): see class documentation.
            age_rating (str): see class documentation.
            imdb_score (float): see class documentation.
        """
        self.movie_id = movie_id
        self.title = title
        self.media_type = media_type
        self.movie_desc = movie_desc
        self.genre = []
        self.age_rating = age_rating
        self.imdb_score = imdb_score

        genre_list = genre[1:-1]
        genre_list = [genre.strip() for genre in genre_list.split(',')]
        self.genre = [genre.strip("'") for genre in genre_list]

    def __str__(self):
        """Returns a string representation of the Movie object.

        Return:
            str: a string representation of the Movie object detailings the movie's attributes.
        """
        return f"""Name: {self.title}\nID: {self.movie_id}\nMedia Type: {self.media_type}\nDescription: {self.movie_desc}\nGenre: {self.genre}\nAge Certification: {self.age_rating}\nIMDB Score: {self.imdb_score}"""

class User():
    """Stores information regarding each users' preferences.
    
    Attributes:
        name (str): the user's name.
        preferences (list): a list of Movie objects pertaining to a user's favorite shows/movies.
    """
    def __init__(self, name):
        """Initializes a User object.

        Args:
            name (str): see class documentation.
        """
        self.name = name
        self.preferences = []
    
    def add_preference(self, movie, database):
        """Adds a media to the user's list of media preferences.

        Args:
            movie (str): the title of the media.
            database (Database): the Database representation of the dataset.

        Raises:
            ValueError: No media was found withint the database under the name provided.
        """
        if movie.lower() not in [m.title.lower() for m in self.preferences]:
            match = database.movies.loc[database.movies['title'].str.contains(movie, case = False)]
            if not match.empty:
                media = Movie(match['id'].iloc[0], match['title'].iloc[0], match['type'].iloc[0], match['description'].iloc[0], match['genres'].iloc[0], match['age_certification'].iloc[0], match['imdb_score'].iloc[0])
                self.preferences.append(media)
            
            else:
                raise ValueError(f"Media with name \"{movie}\" does not exist within the database.")

class Recommender():
    """The main recommendation engine of the system
    
    Attributes:
        common_genres (dict): A dictionary containing the common favorite genres between the user and one of their friends
        user (User): the User object containing info about the user and their preferences.
        friend (User): the User object containing info about the user's chosen friend and their preferences.    """
    def __init__(self, user, friend):
        """Initializes a Recommender class. Sort the dictionary of common genre between two people.
        
        Args: 
            user (User): see class documentation.
            friend (User): see class documentation.
        """
        self.common_genres = {}
        self.user = user
        self.friend = friend        

        common_genres = self.get_common_genres()

        for key, value in sorted(common_genres.items(), key = lambda x: x[1]): 
            self.common_genres[key] = value

    def get_common_genres(self):
        """Searches and ranks the shared genre between two users based on number of match occurances.

        Return:
            dict: a dictionary where the key represents the shared genre between two users and the value represents the amount of matches found for each shared genres.

        Side effects:
            Modifies the value of self.preferences
        """
        user_genres = {}
        friend_genres = {}

        for u in self.user.preferences:
            for genre in u.genre:
                if genre in user_genres.keys():
                    user_genres[genre] += 1
                else:
                    user_genres[genre] = 1
        
        for f in self.friend.preferences:
            for genre in f.genre:
                if genre in friend_genres.keys():
                    friend_genres[genre] += 1
                else:
                    friend_genres[genre] = 1
        
        shared_genres = user_genres.keys() & friend_genres.keys()
        common_genres = {genre: user_genres[genre] + friend_genres[genre] for genre in shared_genres}

        return common_genres

    def get_recommendation(self, database):
        """Get movies/shows recommendation based on the common genres of the user and their friend.

        Args:
            database (Database): a representation of the Database class.
        
        Return:
            DataFrame: the recommended movies/shows.
        """
        df_copy = database.movies.copy()
        search_genres = list(self.common_genres.keys())
        print(search_genres)
        df_copy = df_copy[df_copy['genres'].apply(lambda x: any(genre in x for genre in search_genres))]

        df_copy['num_matches'] = 0
        for i, row in df_copy.iterrows():
            # Split the genres string into a list
            genres_list = row['genres'].strip('][').split(', ')
            genres_list = [genre.strip("'") for genre in genres_list]
            # Count the number of matches with the search genres
            num_matches = sum([genre in search_genres for genre in genres_list])
            # Update the 'num_matches' column for the current row
            df_copy.loc[i, 'num_matches'] = num_matches 

        ranked_df = df_copy.sort_values(by = 'num_matches', ascending = False)
        return ranked_df
       

    def sort_by_score(self, df):
        """Sort the recommendations narrowed down by genre by IMDb scores (descending order).
        
        Args:
            df (DataFrame): a dataframe containing a sorted list of recommendations based on shared genres
            
        Return:
            score_df (DataFrame): recommendations sorted by IMDb scores. 
        """
        score_df = df.sort_values(by = 'imdb_score', ascending = False)
        return score_df

def main(filepath):
    """Starts the recommender system.

    Args: 
        filepath (str): the path to the csv file.

    Side effects:
        print data to the console, including questions to the user, a table of recommended movies, and information regarding a movie
    """
    database = Database(filepath) #creates database object using the filepath
    user_list = [] #empty list to store the user objects entered
    
    while True:
        name = input("Give me the name of a user: ")
        user = User(name) #creates user object with the name entered
        user_list.append(user) #appends the user object into the user_list to store each user object created
        
        while True:
            while True:
                movie = input("Enter a movie name to add it to this user's preference list: ") #prompt to enter movie name
                movie_match = database.movies.loc[database.movies['title'].str.contains(re.escape(movie), flags=re.IGNORECASE)] #finds movies in the database that match the movie entered
                if not movie_match.empty: #if there is a match
                    user.add_preference(movie, database) #adds the movie to the user's preference list using the add_preference() method
                    break
                else:
                    print("Movie not found in database. Please enter another movie") #prints a message if there is not match and prompts the user to try again.
                    
            add_movie = input("Would you like to add another movie? Type \"yes\" or \"no\": ") #asks if they want to add another movie
            while add_movie != 'yes' and add_movie != 'no':
                add_movie = input("Please enter 'yes' or 'no': ")
            
            if add_movie.lower() == 'yes':
                continue #repeats the loop again
            
            elif add_movie.lower() == 'no':
                break #breaks the loop
        
        add_user = input("Would you like to add another user? Type \"yes\" or \"no\": ") #asks if they want to enter a user
        while add_user != 'yes' and add_user != 'no':
            add_user = input("Please enter 'yes' or 'no': ")
        if len(user_list) < 2 and add_user.lower() == "no": #checks if there are less than 2 users added and the response is "no"
            print("A minimum of two users is required") #message stating they need at least 2 users to recommend movies with
            continue #goes to the outer loop where they will be prompt to add a user again
        
        elif add_user.lower() == 'yes':
            continue #goes to the outer loop where they will be prompt to add a user again
        
        elif add_user.lower() == 'no':
            break #exits the outer loop and moves to the matches

    match = False
    while not match:
        first_user = input("Please enter the name of the first user to compare: ")
        for i in user_list:
            if first_user == i.name:
                first_user = i
                match = True
        
    match = False
    while not match:
        second_user = input("Please enter the name of the second user to compare: ")
        for i in user_list:
            if second_user == i.name:
                second_user = i
                match = True
        
    recommender = Recommender(first_user, second_user)
    recommended_movies = recommender.get_recommendation(database)

    num = int(input("Select the number of results to display: "))
    print(recommended_movies.head(num))

    sort = input("Would you like to sort the results by imdb score? Enter 'yes' or 'no': ")
    while sort != 'yes' and sort != 'no':
        sort = input("Please enter 'yes' or 'no': ")
    if sort == 'yes':
        print(recommender.sort_by_score(recommended_movies).head(num))

    response = input("Would you like to see the details of a media? Type 'yes' or 'no': ")
    while response != 'yes' and response != 'no':
        response = input("Please enter 'yes' or 'no': ")

    while response == "yes":
        media_name = input("Please enter the name of the media: ")
        media = database.find_movie(media_name)
        if media is not None:
            print(media)
        else:
            print("Movie not found.")
        response = input("Would you like to see the details of another media? Type 'yes' or 'no': ")
        while response != 'yes' and response != 'no':
            response = input("Please enter 'yes' or 'no': ")


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