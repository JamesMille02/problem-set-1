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

    #opens data
    with open(movie, 'r') as movie_file:
        #saves each line of data
        movie_data_line = [json.loads(line) for line in movie_file]

    #creates dictionary for each actors genre
    actor_genres = {}

    #assigns number for each movie genre each movie the actor has been part of
    #iterates through each line in the movie data
    for single_movie in movie_data_line:
        #saves all genres in the list
        genres = single_movie['genres']
        #iterates through all actors in movie dataset
        for actor_id, actor_name in single_movie['actors']:
            #sees if in dictionary
            if actor_id not in actor_genres:
                #adds actor to set of genres
                actor_genres[actor_id] = {genre: 0 for genre in genres}
            #iterates through the genres
            for genre in genres:
                #checks if genre is in the actors genres
                if genre in actor_genres[actor_id]:
                    #adds 1 in the actor if it is
                    actor_genres[actor_id][genre] += 1
                else:
                    #sets it to one if not
                    actor_genres[actor_id][genre] = 1
    
    #creates dataframe
    cosine_dataframe = pd.DataFrame.from_dict(actor_genres, orient = 'index').fillna(0)
    euclidean_dataframe = pd.DataFrame.from_dict(actor_genres, orient = 'index').fillna(0)

    #renames index to actor id
    cosine_dataframe.index.name = 'Actor_ID'
    euclidean_dataframe.index.name = 'Actor_ID'

    #reshapes dataframe for distance calc
    cosine_vector = cosine_dataframe.loc[query].values.reshape(1 , -1)
    euclidean_vector = euclidean_dataframe.loc[query].values.reshape(1 , -1)

    #calc distance
    cosine_distance = pairwise_distances(cosine_vector, cosine_dataframe.values, metric = 'cosine')
    euclidean_distance = pairwise_distances(euclidean_vector, euclidean_dataframe.values, metric = 'euclidean')

    #adds new column to data frame and flattens it to 1d
    cosine_dataframe['distance'] = cosine_distance.flatten()
    euclidean_dataframe['distance'] = euclidean_distance.flatten()
    #finds 10 closest relationships
    cosine_most_similar_10 = cosine_dataframe.nsmallest(10, 'distance')
    euclidean_most_similar_10 = euclidean_dataframe.nsmallest(10, 'distance')

    print('Top 10 Similar Actors:')
    print(euclidean_most_similar_10)

    #resets index
    cosine_most_similar_10.reset_index(inplace = True)
    #renames index
    cosine_most_similar_10.index.name = 'ID'
    #adds index to the data frame
    cosine_most_similar_10['ID'] = cosine_most_similar_10.index

    #moves the id column so it is first in the dataframe
    columns = ['ID'] + [col for col in cosine_most_similar_10.columns if col != 'ID']
    cosine_most_similar_10 = cosine_most_similar_10[columns]

    #saves current date  and time
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    #saves dataframe as csv
    cosine_most_similar_10.to_csv(f'data/similar_actors_genre_{current_datetime}.csv', index=False)

    print("the list changes based on Euclidean distance by changing how closely related the actors genres are changing the top 10 closest relationships")
    print("comparing the printed euclidean distance results to cosine you will see that the first 4 actors are the same in both; however, the final 6 are different")
