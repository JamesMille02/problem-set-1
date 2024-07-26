import numpy as np
import json
import pandas as pd
import networkx as nx
from datetime import datetime

def network_centrality(movie):
    """Loads the data from the json file and caclulates the centrality
    of each actor. Saves the results to a csv file.

    Args:
        movie(str): path to file of movie data


    """

    #initializaes graph
    network_analysis_graph = nx.Graph()

    #loads data from data folder
    with open(movie, 'r') as in_file:
        #goes through each line in the file
        for line in in_file:
            #saves line as json object
            movie = json.loads(line)
            
            #iterates through each actor in movie
            for actor_id, actor_name in movie['actors']:
                #adds node to graph
                network_analysis_graph.add_node(actor_id, name= actor_name)
            
            #creates list of actor id for movie
            actors = [actor_id for actor_id, _ in movie['actors']]
            #iterates through actor objects
            for i, left_actor_id in enumerate(actors):
                #creates pairwise relationship between each actor in the movie
                for right_actor_id in actors[i+1:]:
                    #checks for existing edge
                    if network_analysis_graph.has_edge(left_actor_id, right_actor_id):
                        #adds  weight if edge exists
                        network_analysis_graph[left_actor_id][right_actor_id]['weight'] += 1
                    else:
                        #adds edge if it does not
                        network_analysis_graph.add_edge(left_actor_id, right_actor_id, weight = 1)
    #print number of nodes
    print("Nodes:", len(network_analysis_graph.nodes))

    #calcs centrality
    centrality = nx.degree_centrality(network_analysis_graph)

    #creates dataframewith centraity items and actors id
    centrality_dataframe = pd.DataFrame(centrality.items(), columns = ['Actor_ID', 'Centrality'])
    
    #saves 10 most central actors
    most_central = centrality_dataframe.nlargest(10, 'Centrality')

    print("10 most central actors")
    print(most_central)

    #adds id for each row in dataframe
    centrality_dataframe['ID'] = centrality_dataframe.index +1

    #moves id column to the front of df
    columns = ['ID'] + [col for col in centrality_dataframe.columns if col != 'ID']
    centrality_dataframe = centrality_dataframe[columns]
    
    #saves current date time
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    #saves dataframe to csv at path
    centrality_dataframe.to_csv(f'data/network_centrality_{current_datetime}.csv', index = False)


#Print the 10 the most central nodes


# Output the final dataframe to a CSV named 'network_centrality_{current_datetime}.csv' to `/data`

