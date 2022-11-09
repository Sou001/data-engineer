
# Récapitulatif des travaux menés

 

## Travail préparatoire

	* démarrer hadoop sur la vm avec le script ~/start-hadoop.sh 
		exécution dans le terminal de : ~/start-hadoop.sh
		
	* créer l'arborescence suivante sur hdfs /data/raw/cities/v1/csv/ sur hdfs 
		hdfs dfs -mkdir -p /data/raw/cities/v1/csv/
		
	* copier le fichier /user/simplon/laposte_hexasmal.csv dans le repertoire /data/raw/cities/v1/csv/ 
		hdfs dfs -put /home/simplon/laposte_hexasmal.csv /data/raw/cities/v1/csv/
		pour vérifier : hdfs dfs -ls /data/raw/cities/v1/csv
		
	* créer une table hive externe nommée cities qui pointe sur le répertoire /data/raw/cities/v1/csv/ 
		* utiliser tblproperties ('skip.header.line.count'='1') lors de la création pour ignore le header du fichier csv.
**/!\ Il faut lancer hive dans le terminal avant l'exzcution des commandes de cette étape & celle d'après**
		 
		create external table cities(code_commune_insee int,
						 nom_de_la_commune string,
						 code_postal string,
						 ligne_5 string,
						 libelle_d_acheminement string ,
						 coordonnees_gps string)
		row format delimited fields terminated by ';'
		stored as TEXTFILE
		location '/data/raw/cities/v1/csv/'
		tblproperties ('skip.header.line.count'='1');

	* vérifier que table pointe correctement sur le fichier en faisant une requête hive
	
		1 - On utilise la commande : "show tables;" , pour vérifier que la table est bien créée
		2 - On utilise la commande : "describe formatted cities;" pour vérifier les informations sur la table
		3 - On utilise la commande : "select * from cities desc limit 2;" pour vérifier si les données correspondent bien avec une comparaison avec les données originales
		

## Lecture de fichier

	* lancer un shell interactif pyspark ou pyspark3 dans le shell interactif
		Dans le terminal, on exécute la commande : pyspark3

	* Lire le fichier csv cities depuis HDFS Lire la table hive cities
		spark.read.csv("hdfs://localhost:9000/data/raw/cities/v1/csv",header=True,sep=";")
		|
		|_résultat : DataFrame[code_commune_insee: string, nom_de_la_commune: string, code_postal: string, ligne_5: string, libelle_d_acheminement: string, coordonnees_gps: string]
		
	* comparer le schéma des deux tables comparer les premières lignes des deux dataframe
		on lit la table hive avec la commande : spark.read.table("cities")
		|
		|_résultat : DataFrame[code_commune_insee: string, nom_de_la_commune: string, code_postal: string, ligne_5: string, libelle_d_acheminement: string, coordonnees_gps: string, year: string]

		Même schéma !
		
	* Créer un dataframe à partir de la liste de personne ci-dessous people_list = [(“john”, “doe”, 34, 75018), (“jane”, “doe”, 42, 64310), (“paul”, “martin”, 14, 33600)] Le noms et type de colonnes sont: FirstName: string LastName: string Age: long ZipCode: long

		1 - On exécute la commande suivante dans le terminal les commandes suivantes (une après l'autre) :
			

			from pyspark.sql.types import StructType, StructField, StringType,LongType

			people_list = [('john', 'doe', 34, 75018), ('jane', 'doe', 42, 64310), ('paul', 'martin', 14, 33600)]
			schema = StructType([ \

				StructField("FirstName",StringType(),True), \

				StructField("LastName",StringType(),True), \

				StructField("Age",LongType(),True), \

				StructField("ZipCode", LongType(), True)

			  ])
	
		2 - df1 = spark.createDataFrame(people_list, schema=schema)

	* écrire le dataframe de personne dans HDFS au format parquet dans le répertoire /raw/people/v1/parquet 
	
		df1.write.parquet('/data/raw/people/v1/parquet')

	** /!\ il va créer tout seul la directory en hdfs & va créer la table ! on vérifie ça avec la commande hdfs : hdfs dfs -ls /data/raw ** 
	
	* écrire le dataframe de personne dans une table hive nommée “people” la table doit être une table interne
		On exécute la commande suivante : df1.write.saveAsTable('people')
		
**/!\ la table sera créée par défaut dans le warehouse hive --> à vérifier avec hive en utilisant : describe formatted people;**



## App

**cf le dossier "spark_cities_app" pour le code de l'app créé avant l'exécution des commandes dans le terminal**

**Tasks :** 
​	* créer un fichier python :
		* créer une spark session
		* créer un dataframe de cities en utilisant le fichier csv cities
		* écrire le dataframe de cities dans HDFS au format parquet dans /experiment/cities/v1/parquet
		* faire en sorte que les données soient écrasées si on relance notre application stopper la spark session

	* supprimer les données cities sur HDFS Lancer votre fichier python en utilisant spark-submit vérifier que les données ont bien été créées

	* créer une application python placer votre fichier de script cities dans le main de votre application packager votre application dans un egg

	* supprimer les données cities sur HDFS Lancer votre egg python en utilisant spark-submit vérifier que les données ont bien été créées

	* Créer une classe cities qui possède une fonction read servant à charger les données cities de hive dans un dataframe. écrire le nom de chaque colonne de la table dans une constante
		
**L'ordre exécution des commandes :**
	
	* Put safemode on off :
		hdfs dfsadmin -safemode leave
	
	* Install requirements : 
		pip3 install -r requirement.txt

	* Create egg file :
		python3 setup.py bdist_egg

	* Launch spark submit :
		spark-submit \
		  --master local \
		  --py-files /home/simplon/Documents/spark/spark_cities_app/dist/SparkCities-0.1-py3.7.egg\
		  /home/simplon/Documents/spark/spark_cities_app/__main__.py
		  
	* On vérifie que nous avons bien créé la table avec :
		hdfs dfs -ls -R /data


## Manipulation de base

	* reprenez votre application spark et créer un nouveau dataframe cities_clean dans le main de votre application qui contiendra 
	  uniquement les colonnes suivantes : 
		* code postal,
		* code insee,
		* nom de la ville,
		* coordonnees gps
		cf script main
		
	* Créer une colonne “dept” qui contient les deux premiers chiffres du code postal. La colonne doit être de type string
		cf script main
		
	* sauvegarder votre dataframe nettoyer sur HDFS dans le dossier /refined/cities/v1/parquet
		cf script main
		
	Pour vérifier la table nous créons une table hive qui lit de la data du file parquet : 
		create external table cities_cleaned(code_commune_insee string, nom_de_la_commune string, 
						     code_postal string, coordonnees_gps string, dept string) 
		stored as parquet
		location '/data/refined/cities/v1/parquet';
		
	Par la suite nous exécutons un : select * from cities_cleaned limit 2;
	
## Test

	* Dans votre application python créer une fonction split_lat_long qui prend en entrée un dataframe et qui renvoie un dataframe. 
	  La fonction doit transformer la colonne coordonnees_gps en deux colonnes latitude et longitude.
	  Les données de latitude doivent être de type double.
	  La colonne coordonnees_gps initiale ne doit plus exister dans le dataframe de sortie
	  
	* écrire un test pour tester la fonction split_lat_long

	* créer une fonction “departement” qui extrait les deux premiers chiffres du code postal dans une colonne dept

	* écrire un test pour tester la fonction departement

	* Reprendre le code de votre application pour enchaîner l’exécution des fonction split_lat_long et departement écrire le résultat dans /refined/cities/v1/parquet

	cf code cities.py pour les fonctions & main.py pour l'ordre d'exécution.
	
	Afin de valider les données, on exécute dans hive les commandes suivantes :
	
	1 - On drop la table qui existe déjà :
			DROP TABLES cities_cleaned;
	
	2 - On la re-crée avec le nouveau schéma : 
	
		create external table cities_cleaned(code_commune_insee string, nom_de_la_commune string, 
						     code_postal string, ligne_5 string, libelle_d_acheminement string, 
						     latitude string, longitude string, dept string) 
		stored as parquet location '/data/refined/cities/v1/parquet';

	3 - On regarde les 3 premières lignes de cette table :
			select * from cities_cleaned limit 3;
			
	4 - launch tests :
			* Code tests est dans : tests/models/test_cities.py
			* On exécute la commande suivante :
				pytest tests/models/test_cities.py
				
**/!\ il faut être dans le dossier du projet sinon il faut penser à mettre tout le chemin vers le fichier de test**
	
## Aggregation & Jointure

	* a partir du dataframe clean_cities créer un nouveau dataframe contenant le nombre de communes par département,
	  sauvegarder le résultat dans un fichier csv unique trié par ordre décroissant de compte (le département contenant 
	  le plus de villes doit être sur la première ligne) sauvegarde le résultat sur hdfs au format csv dans le dossier /refined/departement/v1/csv

	1 - cf code dans main.py & models/cities.py
	2 - Pour vérifier que la table est bien stockée & contient les données que nous souhaitons, on exécute les commandes suivantes   : 
		
		a - On va sur hive :
				Hive
		
		b - On crée la table Hive qui pointe vers où on a stocké notre table de sortie :
		
				create external table departement(dept string, nb_commune int) 
				row format delimited fields terminated by ';' 
				stored as TEXTFILE 
				location '/data/refined/departement/v1/csv';
			
		c - On lit les données : 
				select * from departement_v2 limit 10;
	
## UDF

	* Créer la fonction departement_udf qui a les mêmes paramètres d'entrée et sortie que la fonction département précédente, mais qui calcule correctement
	  le département corse en utilisant une UDF (utiliser le test du chapitre précédent pour tester que votre fonction marche bien.
	  sauvegarder le résultat sur HDFS en csv dans le dossier /refined/departement/v2/csv

		1 - cf code dans main.py & models/cities.py
		2 - Pour vérifier que la table est bien stockée & contient les données que nous souhaitons, on exécute les commandes suivantes   : 
			
			a - On va sur hive :
					Hive
			
			b - On crée la table Hive qui pointe vers où on a stocké notre table de sortie :
			
					create external table departement_v2(dept string, nb_commune int) 
					row format delimited fields terminated by ';' 
					stored as TEXTFILE 
					location '/data/refined/departement/v2/csv';
				
			c - On lit les données : 
					select * from departement_v2 limit 10;
	   
	* Faire une nouvelle fonction departement_fct qui gère le cas de la Corse sans UDF, mais uniquement avec les fonctions disponible sur les colonnes.
	  vous pouvez par exemple utiliser les fonctions : case, when.
	  Une fois les fonctions terminées dans le main de votre application faire un benchmark pour voir laquelle des deux solutions est la plus rapide.
	  
**cf code dans main.py & cities.py**


![image](https://user-images.githubusercontent.com/45198860/200820683-4ebcd2be-6431-4694-a5ae-802e7d9f43d9.png)
		
## Window Function: 
	* À l'aide de window function à chaque ville ajouter les coordonnées GPS de la préfecture du département tel que :
		La préfecture du département se situe dans la ville ayant le code postal le plus petit dans tout le département.
		Pour l’exercice on considère également que la Corse est un seul département (on ne sépare pas la haute corse et la corse du sud).
	 
	* Une fois la préfecture trouvée, calculer la distance relative de chaque ville par rapport à la préfecture:
		On ne cherche pas une distance en km --> calculer la distance moyenne et médiane à la préfecture par département.
	
	* sauvegarder le résultat sur HDFS en csv dans le dossier /refined/departement/v3/csv

**cf code dans main.py & cities.py**

Afin de vérifier les données sauvegardées, nous créons la table hive puis on affiche les résultats :

	create external table departement_v3(dept string, mean_dist float, median_dist float)
	row format delimited fields terminated by ';' 
	stored as TEXTFILE 
	location '/data/refined/departement/v3/csv';

Il y a deux méthodes pour utiliser la distance : 

**Méthode 1 :**
	* On utilise udf avec une fonction python qui utilise des formuls mathématiques pour calculer la distance avec latitude et longetude

**Méthode 2 :**
On utilise la librairie geopy. Pour cela il faut créer un env dans lequel on installera les librairies qu'il nous faut.
Par la suite on met à disposition de spark ces informations dans "spark-submit" :

	* Création de l'env :
		virtualenv myenv -p /usr/bin/python3
	
	* Activation de l'env :
		source myenv/bin/activate
		
	* Lancer l'installation de tous les libs dont on a besoin sachant que geopy en fait partie maintenant :
		pip3 install -r requirements.txt
	
	* Utiliser le module geopy pour le calcul de distance :
		cf code dans main.py & cities.py
	
	* Spark submit : 
		spark-submit \
		  --master local \
		  --conf spark.pyspark.python=/usr/bin/python3 \
		  --py-files /home/simplon/Documents/spark/spark_cities_app/dist/SparkCities-0.1-py3.7.egg\
		  /home/simplon/Documents/spark/spark_cities_app/__main__.py
	
	* Tester avec Hive  :
		create external table departement_v4(dept string, mean_dist float, median_dist float)
		row format delimited fields terminated by ';' 
		stored as TEXTFILE 
		location '/data/refined/departement/v4/csv';
		
		select * from departement_v4 limit 10;
		
##  Scala

	réécrire votre application en scala
	
