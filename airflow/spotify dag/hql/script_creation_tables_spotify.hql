CREATE EXTERNAL TABLE IF NOT EXISTS tracks(playlist_id STRING,
							                 track_id STRING,
							                 artist_id STRING,
							                 date_exec TIMESTAMP)
		
    row format delimited fields terminated by ','
    stored as TEXTFILE
	location '/data/spotify/tracks/csv';
	
	
CREATE EXTERNAL TABLE IF NOT EXISTS artists(name STRING,
							                  id STRING,
							                  date_exec TIMESTAMP,
							                  popularity int)

    row format delimited fields terminated by ','
	stored as TEXTFILE
	location '/data/spotify/artists/csv';
