
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
		  ├── parquet
		  ├── csv
		  └── header

	Application dans notre cas au même niveau que le "/user" : 
		data 
		  └──2022
			  ├── parquet
			  ├── csv
			  └── header
		
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
		location '/data/2022/parquet';

	* Utiliser Hive pour peupler la table cities_2022_parquet à partir de la table cities_2022 
		INSERT INTO TABLE cities_2022_parquet SELECT * FROM cities_2022;
		
			   || Pour vérifier on peut utiliser : select * from cities_2022_parquet; ||
			   
		Optionnel
	* dans Hive définir une table cities partitionné par année qui contiendra les données du fichiers cities_2022 au format parquet :
		
			CREATE TABLE cities(
					code_commune_insee STRING,
					nom_de_la_commune STRING,
					code_postal STRING,
					ligne_5 STRING,
					libelle_d_acheminement STRING,
					coordonnees_gps STRING)
			PARTITIONED BY(year string)
			stored as PARQUET
			location '/data';
			
	* ajouter la partition pour l’année 2022 & peupler la table à l’aide de la table cities_2022 
			
			INSERT INTO TABLE cities PARTITION(year='2022') SELECT * FROM cities_2022;
			
#### Cheminement des tâches avec des photos :

	1 - Identification du fichier & copier en local + générer les fichiers (header & corps) :
![identification_fichier](https://user-images.githubusercontent.com/45198860/195123088-c420e8cb-cbdd-4125-8f08-2765f0e16c98.PNG)
![copie_fichier](https://user-images.githubusercontent.com/45198860/195123163-9bea2fee-1aed-4b25-95cb-2ce80c55e4b4.PNG)
![generated_files](https://user-images.githubusercontent.com/45198860/195123224-43546ac8-2cf0-4ed2-bf98-1d8322f8105b.PNG)

	2 - Création de l'arborescence
![arbo1](https://user-images.githubusercontent.com/45198860/195123297-96843176-dca6-41b1-b44f-c0d627c34f48.PNG)
![arbo2](https://user-images.githubusercontent.com/45198860/195123335-884b14dd-d1a6-4ac3-b5fd-c664e05d546c.PNG)
![image](https://user-images.githubusercontent.com/45198860/195123567-eb86f457-fcb0-4f21-bb98-1f20b314765e.png)

	3 - Création group & user (data_analyst) + directory data_analyst dans user + copier fichier corps + accès
![image](https://user-images.githubusercontent.com/45198860/195124640-2261624d-17ec-4ad5-ba48-9c8f9b95a178.png)
![image](https://user-images.githubusercontent.com/45198860/195124927-f63d66b6-6df0-4f61-927f-5ed138761c69.png)


	4 - Création des tables avec Hive
	
