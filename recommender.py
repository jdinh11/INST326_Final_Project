class Database():
    """A class for storing a dataframe of the dataset

    Attributes
        movie_id (str): the media's id
        title (str): the media's title
        type (str): the type of media (movie or show)
        gernes (list): the media's list of associated gernes
        age_ratings (str): the media's age restrictions (if any)
        imdb_score (int): the media's imdb ratings 
    """
    def __init__(filepath):
        """Initializes a Database class

        Args: 
            filepath (str): the filepath to the dataset
        """
        pass

    def dataframe():
        """A dataframe containing a set of data regarding different Netflix medias

        Args:
            filepath (str): the filepath to the dataset

        Return:
            a dataframe version of the dataset
        """
        pass

    def processing():
        """Process the data and get rid/modify potential insuffiencient rows within the dataframe

        Args:
            datas (tuple): rows of data for processing

        Return:
            the polished rows of data
        """
        pass

    def check_movie(input):
        """Check if the user's movies exists within the dataset

        Args: 
            input (string): the movie's name

        Return:
            the movie's name if it passes the check

        Raise Error:
            Error: the movie does not exist within the dataset
        """
        pass

class Movie():
    """A class for storing information regarding a list of Netflix medias

    Attributes:
        movie_id (str): the media's id
        title (str): the media's title
        type (str): the type of media (movie or show)
        gernes (list): the media's list of associated gernes
        age_ratings (str): the media's age restrictions (if any)
        imdb_score (int): the media's imdb ratings 
    """
    def __init__(self, movie):
        """Initializes a Movie class

        Args:
            movie (str): the name of a movie
        """
        pass

    def attributes(path):
        """Get the media's attributes

        Args:
            path: the path to the dataset
        """
        pass

    def get_recommendations(title):
        """Get recommendations based on friend's favorite movies

        Args: 
            title (str): the name of a movie
        """
        pass

def format_results(recommendations):
    """Format the recommendation list for the user
    Args:
        recommedations (list): the list recommended movies
    
    Return:
        the recommendation displayed in the formatted structure
    """
    pass

def main(filepath):
    """Enable the recommended

    Args: 
        filepath (str): the path to the csv file
    """

def parse_args():
    """Takes a list of strings from the command prompt and passes them through as arguments
    
    Args:
        args_list (list) : the list of strings from the command prompt
    
    Returns:
        args (ArgumentParser)
    """
    pass

if __name__ == "__main__":
    main()