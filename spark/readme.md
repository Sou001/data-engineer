
# Récapitulatif des travaux menés


### Notes : 

### Travail préparatoire

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
		3 - On utilise la commande 
		

### Lecture de fichier

	* lancer un shell interactif pyspark ou pyspark3 dans le shell interactif
		Dans le terminal, on exécute la commande : pyspark3

	* Lire le fichier csv cities depuis HDFS Lire la table hive cities
		spark.read.csv("hdfs://localhost:9000/data/raw/cities/v1/csv",header=True,sep=";")
		|
		|_résultat : DataFrame[code_commune_insee: string, nom_de_la_commune: string, code_postal: string, ligne_5: string, libelle_d_acheminement: string, coordonnees_gps: string]
		
	* comparer le schéma des deux tables comparer les premières lignes des deux dataframe
		on lit la table hive avec la commande : spark.read.table("cities")
		|
		|_résultat :DataFrame[code_commune_insee: string, nom_de_la_commune: string, code_postal: string, ligne_5: string, libelle_d_acheminement: string, coordonnees_gps: string, year: string]

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
	
	