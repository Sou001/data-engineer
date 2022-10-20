
# Récapitulatif des travaux menés pour la mise en place 



#### Mise en place des premoiers dags

Il y a deux dags :
	
	* hourly_launch.py :
	
		se lançant toutes les heures + démarrant ce matin à 9H, il exécute les tâches suivantes :
	
		* Dummy operator start 
		* sensor pour détecter l'arrivé d'un fichier
		* bash operator nommé "list" et exécute la commande "ls"
		* Python operator "hello" :
			* écrit un fichier contenant le mot "world" et contenant la date d'execution du workflow
			* Génère un fichier dont le nom contient la date d'exécution du workflow
			* Utilise une variable airflow ( créée à la main dans l'ui) & la fait passer à la tâche suivante 
		* bash operator nommé "printvalue" va affichr la variable transmise par la tâche d'avant (xcom)
		* bash operators sleep 10 s & sleep 15s en parralèle
		* Dummy operator join 

	
	* db_dag.py :
		créer et utiliser des connections airflow pour se connecter à une base de donnée (postgresql)
		* utilisation du PostgresOperator pour se connecter à postgres et créer une table ainsi que l'alimenter 
	
![image](https://user-images.githubusercontent.com/45198860/196931041-d6cd75f7-67c1-4ff3-82c6-8922b63fb459.png)
