
# Récapitulatif des travaux menés

 

## Travail préparatoire - Installation d'Elasticsearch et outils nécessaires au dev/viz

	* Télécharger :
		* Elasticsearch : https://www.elastic.co/fr/downloads/past-releases/elasticsearch-7-17-7
		* kibana 		: https://www.elastic.co/fr/downloads/past-releases/kibana-7-17-7
		* Cerebro 		: https://github.com/lmenezes/cerebro/releases


	* Elasticsearch - nosql search engine - :
		
		* Déziper le tar Elasticsearch & extraire les fichiers
	
		* Lancer le serveur Elasticsearch avec un terminal :
			
			* Aller sur le dossier : 
				cd elasticsearch-7.17.7
			* Exécuter : 
				$ELASTIC bin/elasticsearch
					
		* Etudier l'état du serveur elasticsearch :
			* Avec un navigateur - webservice rest - :
				http://localhost:9200/?pretty
					
			* Via un terminal :
				curl -X GET http://localhost:9200

		**/!\ Note sur les méthodes pour shutdown le serveur**
			1 - curl -X OST 'http://localhost:9200/_shutdown' 
			2 - ctrl + c 

-----------------------
	* Cerebro - outil d'administration Web d'Elasticsearch - :
	/ Permet de visualiser l’ensemble de noeuds, avec les informations comme l’usage de la mémoire, espace disque, cpu et load average./
		
		* Déziper le tar Cerebro & extraire les fichiers
		
		* Via terminal :
			* aller sur le dossier 
			* Donner les droits d'exécution :
				sudo chmod u+x bin/cerebro
			* Exécuter :
				bin/cerebro
		
		* Du navigateur lancer : 
			http://localhost:9000/

-----------------------		
	* Kibana - Data viz tool - :
		* Déziper le tar Kibana & extraire les fichiers
		
		* Sur le termnial, aller sur le dossier Kibana et exécuter :
			$KIBANA bin/kibana

		* Ouvrir dans le navigateur :
			http://localhost:5601


## Partie 1 - Importer les données dans Elasticsearch 

Objectif : Importer les données dans dataset/movies.json dans Elasticsearch & vérifier leur état

Le fichier que nous allons utilisé, est : "dataset/movies.json"
	** Il faut vérifier avant que le fichier json contient une ligne du type : : {"index":{"_index": "MA BASE","_id":1}} **
	** Dans notre cas on a : {"index":{"_index": "movies","_type":"movie","_id":1}} ** 

		
**1 - Importer les donnés :**

	* En utilisant Curl dans le terminal :
	
		* curl -H "Content-Type: application/json" -XPUT "localhost:9200/_bulk" --data-binary @movies.json
	
	* En utilisant Kibana :
		* Aller sur Menu/Management/Integrations
		* Choisir “upload a file”
		* Drag and drop le fichier “movies.json”
		* Cliquer sur “Import” en bas à gauche
		* Donner un nom à l’index “movies”
	
**2 - Vérifier les données :**

	* Avec le serveur Elasticsearch : 
		http://localhost:9200/movies/_search
		
		On regarde la partie 'hits'. On a les objets : 0,1,... qui correspondent aux documents/objets json
		
	* Avec curl : 
		curl -XGET http://localhost:9200/movies/movie/1
		
		Renvoie le premier hit
		
	* Kibana :
		* Aller dans menu/management/dev tools (correspond au lien : http://localhost:5601/app/dev_tools#/console)
		* Exécuter : GET movies/movie/1 , pour le 1er hit
		
		
		
		
## Partie 2 - Requêtes simples

** Le but de cette partie est de faire des requêtes simples pour se familiariser avec rest queries.**

	cf le notebook "elastic_stack_simple_queries"


## Partie 3 - index & crud

** Le but de cette partie est de faire des manipulations de création d'index & insértion des données (create, read, update, delete)**

	cf le notebook "elastic_stack_index_crud"


## Partie 4 - Aggregation

** Le but de cette partie est de faire des requêtes complexes type aggrégations pour aller plus loins dans la maitrise de ce type de requêtes.**

	cf le notebook "elastic_stack_aggs"
