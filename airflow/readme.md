
# Récapitulatif des travaux menés pour la mise en place 



#### Mise en place du premier DAG spotify

Execution du code spotify chaque jour à 7 :
	* Connexion à l'api Spoityf
	* Récupérer les informations sur les tracks & artists de la liste des playlists définiée
	* Stocker ces données dans le dossier sortie **sans header**
	
Le dag contient 2 tâches seulement à ce moment

#### Création de l'arborescence HDFS

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
			  
![image](https://user-images.githubusercontent.com/45198860/195827848-e2b6e859-e981-4c4c-aff8-2c4a47a57bc1.png)

On dépose dans le header de chacune des tables, un fichier contenant les noms des colonnes des tables. 
![image](https://user-images.githubusercontent.com/45198860/195828170-d5316c84-c826-4095-844c-1e1c35babf71.png)

![image](https://user-images.githubusercontent.com/45198860/195828524-65710a69-d298-4431-bfa0-b24e1049bacb.png)

#### Création des tables Hive

* On crée les tables avec "create external table" (cf dans dossier hql dans dossier dags)





