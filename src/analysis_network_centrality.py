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

    network_analysis_graph = nx.Graph()

    with open(movie, 'r') as in_file:
        for line in in_file:
            movie = json.loads(line)
            
            for actor_id, actor_name in movie['actors']:
                network_analysis_graph.add_node(actor_id, name= actor_name)
            
            actors = [actor_id for actor_id, _ in movie['actors']]
            for i, left_actor_id in enumerate(actors):
                for right_actor_id in actors[i+1:]:
                    if network_analysis_graph.has_edge(left_actor_id, right_actor_id):
                        network_analysis_graph[left_actor_id][right_actor_id]['weight'] += 1
                    else:
                        network_analysis_graph.add_edge(left_actor_id, right_actor_id, weight = 1)

    print("Nodes:", len(network_analysis_graph.nodes))

    centrality = nx.degree_centrality(network_analysis_graph)

    centrality_dataframe = pd.DataFrame(centrality.items(), columns = ['Actor_ID', 'Centrality'])
    
    most_central = centrality_dataframe.nlargest(10, 'Centrality')

    print("10 most central actors")
    print(most_central)

    centrality_dataframe['ID'] = centrality_dataframe.index +1

    columns = ['ID'] + [col for col in centrality_dataframe.columns if col != 'ID']
    centrality_dataframe = centrality_dataframe[columns]
    
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file  = f'data/network_centrality_{current_datetime}.csv'

    centrality_dataframe.to_csv(csv_file, index = False)


#Print the 10 the most central nodes


# Output the final dataframe to a CSV named 'network_centrality_{current_datetime}.csv' to `/data`

