import requests
import os
import json
import analysis_network_centrality
import analysis_similar_actors_genre



def download_imdb_data():
    """Downloads the datafrom the imdb github file.
    """
    
    imdb_url = 'https://raw.githubusercontent.com/cbuntain/umd.inst414/main/data/imdb_movies_2000to2022.prolific.json'

    #file for the data to be saved
    json_file = 'data/imdb_movies_2000to2022.prolific.json'

    os.makedirs(os.path.dirname(json_file), exist_ok=True)

    response = requests.get(imdb_url)

    data = response.text.strip().split('\n')
    json_data = '[' + ','.join(data) + ']'

    with open(json_file, 'w') as f:
        f.write(json_data)



# Call functions / instanciate objects from the two analysis .py files
def main():
    download_imdb_data()
    analysis_network_centrality.network_centrality('/data/imdb_movies_2000to2022.prolific.json')
    analysis_similar_actors_genre.similarity_analysis('/data/imdb_movies_2000to2022.prolific.json', 'nm1165110')



if __name__ == "__main__":
    main()