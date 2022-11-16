
# Récapitulatif des travaux menés

 

## Travail préparatoire

	* Télécharger :
		* Elasticsearch : https://www.elastic.co/fr/downloads/past-releases/elasticsearch-7-17-7
		* kibana 		: https://www.elastic.co/fr/downloads/past-releases/kibana-7-17-7
		* Cerebro 		: https://github.com/lmenezes/cerebro/releases


	* Elasticsearch :
		
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

	* Cerebro - Interface pour visualiser la data dans Elasticsearch - :
		
		* Déziper le tar Cerebro & extraire les fichiers
		
		* Via terminal :
			* aller sur le dossier 
			* Donner les droits d'exécution :
				sudo chmod u+x bin/cerebro
			* Exécuter :
				bin/cerebro
		
		* Du navigateur lancer : 
			http://localhost:9000/
		
	* Kibana - Data viz tool - :
		* Déziper le tar Kibana & extraire les fichiers
		
		* Sur le termnial, aller sur le dossier Kibana et exécuter :
			$KIBANA bin/kibana

		* Ouvrir dans le navigateur :
			http://localhost:5601

## Partie 1 - Importer les données dans Elasticsearch 

Objectif : Importer les données dans dataset/movies.json dans Elasticsearch :

** Il faut vérifier avant que le fichier json contient une ligne du type : : {"index":{"_index": "MA BASE","_id":1}} **
** Dans notre cas on a : {"index":{"_index": "movies","_type":"movie","_id":1}} ** 
	
1 - Importer les donnés : 

	* En utilisant Curl :
	
		* curl -H "Content-Type: application/json" -XPUT "localhost:9200/_bulk" --data-binary @movies.json
	
	* En utilisant Kibana :
	
2 - Vérifier les données :

	* Avec le serveur Elasticsearch : http://localhost:9200/movies/_search
	
	* Avec curl : curl -XGET http://localhost:9200/movies/movie/1 