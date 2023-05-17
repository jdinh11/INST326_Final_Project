# Movie Recommendation System
Our project is a Movie Recommendation System that will help users find reccommendations based on their movie preferences and their friend's as well. This system will allow users to add their movie preferences as well as their friends', and then allows the user to select two users to compare preferences with and return the recommended movies to watch. Addtionally, the user can enter the number of recommended movies they want returned back to them in order to avoid overwhelming them.

# How to run the program in the command line
First, enter the name of the python file (recommender.py) and the csv file (titles.csv). Next, it will ask to enter the user's name and then their favorite movie. It will then ask if you would like to add more movies. You can type "yes" and keep adding more movies until you type "no". It will then ask if you would like to add another user in which the user can type "yes" and repeat the process of adding their movies or type "no". It will then ask to pick 2 users' you would like to compare movies with. Finally, it will ask how many results you want displayed in which the user can enter an integer and it will print out a dataframe of movies containing the content recommended for the 2 users.

# How to interpret the output of the program
The output of the program is a dataframe - of length specified by the user - of movie recommendations for the user. This dataframe will be ordered based on whether or not the media contains genres similar between the two users and by imbd scores. Additionally, the dataframe will contain information on the media such as the title of the media, the age rating, the genres, and the imdb score. If the user wants more information, they can prompt the program to give more information (ex. description) of the media. 
A user can interpret the output of the program by going through the selection of recommendations and seeing if they would be interested in any of the options based on the information provided by the dataframe. 

# Bibliography 
Bansal, Shivam. 'Netflix Movies and TV Shows". Kaggle.com. 
    Accessed 21 April 2023. https://www.kaggle.com/datasets/shivamb/netflix-shows

    This dataset was created by Shivam Bansal and posted on Kaggle.com and is updated regularly. This dataset contains information on Netflix's over 8000 movies and TV shows (as od mid-2021). The tabular dataset has listings of all the movies and TV shows with details such as name, cast, directors, ratings, release year, duration, etc. 
    We used this dataset in order to get information on Netflix's content and information on their movies and TV shows without having to webscrape the entire website itself. We call the dataset with a CSV file ('titles.csv') and filter through the dataset in order to narrow it the vast content down to characteristics and factors that we need in order to best make a recommendation for the user. 