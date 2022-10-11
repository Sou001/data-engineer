

CREATE TABLE cities_2022(code_commune_insee int,
						 nom_de_la_commune string,
						 code_postal string,
						 ligne_5 string,
						 libelle_d_acheminement string ,
						 coordonnees_gps string)
row format delimited fields terminated by ';'
stored as TEXTFILE
location '/data/2022/csv';


CREATE External TABLE cities_2022_external(code_commune_insee int,
										   nom_de_la_commune string,
										   code_postal string,
										   ligne_5 string,
										   libelle_d_acheminement string ,
										   coordonnees_gps string)
row format delimited fields terminated by ';'
stored as TEXTFILE
location '/data/2022/csv';
					

CREATE TABLE cities_2022_parquet(
				code_commune_insee STRING,
				nom_de_la_commune STRING,
				code_postal STRING,
				ligne_5 STRING,
				libelle_d_acheminement STRING,
				coordonnees_gps STRING)
stored as PARQUET
location '/DATA/2022/PARQUET';
INSERT INTO TABLE cities_2022_parquet SELECT * FROM cities_2022;

CREATE TABLE cities(
				code_commune_insee STRING,
				nom_de_la_commune STRING,
				code_postal STRING,
				ligne_5 STRING,
				libelle_d_acheminement STRING,
				coordonnees_gps STRING)
PARTITIONED BY(year string)
stored as PARQUET
location '/DATA';
					
INSERT INTO TABLE cities PARTITION(year='2022') SELECT * FROM cities_2022;