
# Récapitulatif des travaux menés pour la mise en place 



#### Mise en place du premier DAG spotify

Execution du code spotify chaque jour à 7 :
	* Connexion à l'api Spoityf
	* Récupérer les informations sur les tracks & artists de la liste des playlists définiée
	* Stocker ces données dans le dossier sortie sans header
	
Le dag contient 2 tâches seulement à ce moment

#### Création de l'arborescence

Création de l'arborescence HDFS pour stocker l'historique des tables tracks & artistes.

On utilise le dossier "data"  déjà créer pour le brief sur hadoop & on ajoute les dossiers tracks & artists

		data 
		  └──tracks
			├── parquet
			  ├── csv
			  └── header
		  └──tracks
			  ├── parquet
			  ├── csv
			  └── header
			  
