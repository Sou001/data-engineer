
# Récapitulatif des travaux menés


### Notes : 
Les commandes hadoop/hdfs pour faire des vérifications :
  * hdfs dfs -ls directory --> exemple hdfs dfs -ls /data

Avec hive :
  * show tables;
	* describe formatted name_table;

### Tâches : 
#### Temps 1 - définir une arborescence pour le stockage dans du fichier + Temps 2 - restitution 

	L'arborescence convenue est : 
				AAAA 
					parquet
					csv
					header
			
				
#### Temps 3 - Travail Individuel
		
			* Pour lancer le système de stockage : 
				./start-hadoop.sh
			
			* Récupérer le fichier depuis HDFS sur votre poste local :
				hdfs dfs -get laposte_hexasmal.csv /home/simplon

			* Extraire du fichier la 1er ligne contenant l’en-tête dans un fichier nommé cities_headers.txt
				head -n1 laposte_hexasmal.csv > cities_headers.txt
				
			* En local créer un fichiers cities_2022.csv ne contenant pas la ligne d’en-tête :
				tail -n+2 laposte_hexasmal.csv > cities_2022.csv
				
			* Sur HDFS créer l’arborescence cible qui contiendra votre fichier : 
				hdfs dfs -mkdir /data/2022
				hdfs dfs -mkdir /data/2022/header
				hdfs dfs -mkdir /data/2022/parquet
				hdfs dfs -mkdir /data/2022/csv
				
			* Envoyer ce fichier sur HDFS :
				hdfs dfs -put cities_headers.txt /data/2022/header
				hdfs dfs -put cities_2022.csv /data/2022/csv


		* Optionnel : 
			* sur la machine local créer un groupe data_analyst :
				sudo groupadd data_analyst
				
			* sur la machine local créer un utilisateur data_analyst et le ratacher au groupe data_analyst :
				sudo useradd -g data_analyst data_analyst
			
			* créer un répertoire data_analyst dans le dossier /user de HDFS :
				hdfs dfs -mkdir /user/data_analyst
			
			* sur HDFS changer le propriétaire et groupe du dossier /user/data_analyst pour data_analyst :
				hdfs dfs -chown data_analyst:data_analyst /user/data_analyst
				
			* déplacer le fichier cities_2022.csv et faire en sorte que seule les data_analyst puissent y accéder en lecture uniquement
				hdfs dfs -put -f Documents/cities_2022.csv  /user/data_analyst
				hdfs dfs -chmod 0444 /user/data_analyst/cities_2022.csv
				
				
				
#### Temps 4 -  Hive
			* dans Hive créer une table cities_2022 qui pointe sur votre fichier cities_2022.csv
				* Internal :
					CREATE TABLE cities_2022(code_commune_insee int,
											 nom_de_la_commune string,
											 code_postal string,
											 ligne_5 string,
											 libelle_d_acheminement string ,
											 coordonnees_gps string)
					row format delimited fields terminated by ';'
					stored as TEXTFILE
					location '/data/2022/csv';
					
				* External :
					CREATE External TABLE cities_2022_external(code_commune_insee int,
											 nom_de_la_commune string,
											 code_postal string,
											 ligne_5 string,
											 libelle_d_acheminement string ,
											 coordonnees_gps string)
					row format delimited fields terminated by ';'
					stored as TEXTFILE
					location '/data/2022/csv';
					
			* dans Hive créer une table cities_2022_parquet qui stockera les données de cities_2022 mais au format parquet
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


			* Utiliser Hive pour peupler la table cities_2022_parquet à partir de la table cities_2022
		
		Optionnel
			* dans Hive définir une table cities partitionné par année qui contiendra les données du fichiers cities_2022 au format parquet +
				ajouter la partition pour l’année 2022 + peupler la table à l’aide de la table cities_2022 :
				
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
