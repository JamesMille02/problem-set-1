'''
PART 2: SIMILAR ACTROS BY GENRE
Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

#Write your code below

import json
import pandas as pd
from sklearn.metrics import pairwise_distances
from datetime import datetime

def similarity_analysis(movie, query):
    """Calculates the most similar actors based on genre.
    
    Args:
        movie(str): path to movie data set
        query(str): actor id for querying the graph
    
    Prints:
        similar_10(df): 10 most similar actors to one specfic actor
    """

    with open(movie, 'r') as movie_file:
        movie_data_line = [json.loads(line) for line in movie_file]

    actor_genres = {}

    for single_movie in movie_data_line:
        genres = single_movie['genres']
        for actor_id, actor_name in single_movie['actors']:
            if actor_id not in actor_genres:
                actor_genres[actor_id] = {genre: 0 for genre in genres}
            for genre in genres:
                if genre in actor_genres[actor_id]:
                    actor_genres[actor_id][genre] += 1
                else:
                    actor_genres[actor_id][genre] = 1

    dataframe = pd.DataFrame.from_dict(actor_genres, orient = 'index').fillna(0)

    dataframe.index.name = 'Actor_ID'

    vector = dataframe.loc[query].values.reshape(1 , -1)

    euclidean_distance = pairwise_distances(vector, dataframe.values, metric = 'euclidean')

    dataframe['distance'] = euclidean_distance.flatten()
    most_similar_10 = dataframe.nsmallest(10, 'distance')

    print('Top 10 Similar Actors:')
    print(most_similar_10)

    most_similar_10.reset_index(inplace = True)
    most_similar_10.index.name = 'ID'
    most_similar_10['ID'] = most_similar_10.index

    columns = ['ID'] + [col for col in most_similar_10.columns if col != 'ID']
    most_similar_10 = most_similar_10[columns]

    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    most_similar_10.to_csv(f'data/similar_actors_genre_{current_datetime}.csv', index=False)
