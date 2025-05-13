"""Identify the most popular movie ratings based on data in two CSV files."""

from argparse import ArgumentParser
import pandas as pd
import sys

def best_movies(movie_path, ratings_path):
    """ Returns movies sorted by average rating in descending order.
    
    Args:
        movie_path(list of str): the path to a file of movie data.
        ratings_path(list of str): the path to a file of rating data.
    
    Returns:
        Series: a sorted version of the average rating series.
    """
    #reading each CSV file into its own DataFrame
    movie_df = pd.read_csv(movie_path)
    ratings_df = pd.read_csv(ratings_path)

    #inner merging the DataFrames using the "item id" and "movie id" column
    merged_df= pd.merge(movie_df, ratings_df, left_on='movie id', right_on='item id', how='inner')
    
    #grouping by the "movie title" column and finding the average value of the "rating" column
    average_ratings = merged_df.groupby('movie title')['rating'].mean()
    
    return average_ratings.sort_values(ascending=False)

def parse_args(arglist):
    """ Parse command-line arguments.
    
    Args:
        arglist (list of str): a list of command-line arguments.
    
    Returns:
        namespace: the parsed command-line arguments as a namespace with
        variables movie_csv and rating_csv.
    """
    parser = ArgumentParser()
    parser.add_argument("movie_csv", help="CSV containing movie data")
    parser.add_argument("rating_csv", help="CSV containing ratings")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    movies = best_movies(args.movie_csv, args.rating_csv)
    print(movies.head())
