
                                ### DAG FOR API SPOTIFY ### 

# The DAG object
from airflow import DAG

# time libs
from datetime import timedelta, datetime

# Operators
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

import pandas as pd



## function that get the date of execution
def df_exec_saver(**context):
    return context["execution_date"].strftime("%Y-%d-%m")


## function to return ecart entre deux tracks df
## dt_previous_tracks, dt_current_tracks
def in_out(**kwargs):
    
    dt_previous_tracks, dt_current_tracks = kwargs["dt_previous_tracks"], kwargs["dt_current_tracks"]
    
    print("in here ",dt_current_tracks)
    path="/home/simplon/airflow/spotify_playlist/sorties/tracks_put_"+dt_current_tracks+".csv"
    
    current_tracks = pd.read_csv("/home/simplon/airflow/spotify_playlist/sorties/tracks_"+
                                dt_current_tracks+".csv",
                                header=None,
                                names=["playlist_id","track_id","artist_id","date"])

    path_previous_tracks = "/home/simplon/airflow/spotify_playlist/sorties/tracks_"+dt_previous_tracks+".csv"

    ## in case we already have history
    try :
        previous_tracks = pd.read_csv(path_previous_tracks, header=None,
                                    names=["playlist_id","track_id",
                                           "artist_id","date"]).drop("track_id",
                                    axis=1).drop_duplicates()

        current_tracks = current_tracks.drop("track_id", axis=1).drop_duplicates()

        outer = previous_tracks.merge(current_tracks, how='outer', indicator=True)

        removed_artist = outer[(outer._merge=='left_only')].drop('_merge', axis=1)
        removed_artist["status"] = "out"
        new_artist = outer[(outer._merge=='right_only')].drop('_merge', axis=1)
        new_artist["status"] = "in"

        pd.concat([removed_artist, new_artist]).to_csv(path)

    ## in case we don't have history, we create it in order 
    except :
        current_tracks.to_csv(path)
        pd.DataFrame([]).to_csv(path_previous_tracks)


with DAG('spotify_operator',
		default_args={'owner': 'sousou'},
		description='Launch connection to api, collect data, merge and history',
		schedule_interval=timedelta(days=1),
		start_date=datetime(2022,10,22,9),
		catchup=False,
		tags=['Spotify, api']) as dag :

    ## task to get tracks - exec py script
	get_tracks = BashOperator(task_id='get_tracks', 
                              bash_command="python3 /home/simplon/airflow/spotify_playlist/get_tracks.py")
	
    ## task to get artists - exec py script
	get_artists = BashOperator(task_id='get_artists', 
                               bash_command="python3 /home/simplon/airflow/spotify_playlist/get_artists.py")

    ## going to merge history with now for tracks
	in_out_task = PythonOperator(task_id='in_out_task', 
                                    python_callable=in_out,
                                    provide_context=True,
                                    op_kwargs={"dt_previous_tracks": "{{ds}}",
                                               "dt_current_tracks": "{{tomorrow_ds}}"})

    ## task to put files of tracks in hdfs
	put_new_tracks = BashOperator(task_id="put_new_tracks",
                        bash_command='hdfs dfs -put /home/simplon/airflow/spotify_playlist/sorties/tracks_put_{{tomorrow_ds}}.csv /data/spotify/tracks/csv')

    ## task to put files of artists in hdfs
	put_new_artists = BashOperator(
                        task_id="put_new_artists",
                        bash_command='hdfs dfs -put /home/simplon/airflow/spotify_playlist/sorties/artists_{{tomorrow_ds}}.csv /data/spotify/artists/csv')

    ## part where we clean unusefull data for the next run
    ## Clean the data of the day before because in the next run, which is tomorrow, we'll only need the data 
    ## of today as history
	clean_tracks_day_before = BashOperator(
                        task_id="clean_tracks_day_before",
                        bash_command='rm /home/simplon/airflow/spotify_playlist/sorties/tracks_{{ds}}.csv')
    
    ## cleaning the in and out calculated data
	clean_tracks_inout = BashOperator(
                        task_id="clean_tracks_inout",
                        bash_command='rm /home/simplon/airflow/spotify_playlist/sorties/tracks_put_{{tomorrow_ds}}.csv')

    ## Cleaning the artists data since we don't need the history
	clean_artists = BashOperator(
                        task_id="clean_artists",
                        bash_command='rm /home/simplon/airflow/spotify_playlist/sorties/artists_{{tomorrow_ds}}.csv')

get_tracks >> get_artists >> in_out_task >> [put_new_tracks,put_new_artists] >> clean_artists >> [clean_tracks_day_before,clean_tracks_inout]
