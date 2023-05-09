import pytest
import pandas as pd
from recommender import Database, Movie, User

@pytest.fixture
def database():
    titles = Database("Titles.csv")
    return titles

@pytest.fixture
def movie():
    movies = Movie("tm70993", "Life of Brian", "MOVIE", "Brian Cohen is an average young Jewish man, but through a series of ridiculous events, he gains a reputation as the Messiah. When he's not dodging his followers or being scolded by his shrill mother, the hapless Brian has to contend with the pompous Pontius Pilate and acronym-obsessed members of a separatist movement. Rife with Monty Python's signature absurdity, the tale finds Brian's life paralleling Biblical lore, albeit with many more laughs.", ['comedy','GB'], "R", 7.8)
    return movies

@pytest.fixture
def user(database):
    user = User("Gerald")
    user.add_preference("Life of Brian", database)
    return user


