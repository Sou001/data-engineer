
# Récapitulatif des travaux menés pour la mise en place 



### Manipuler des DB nosql avec MangoDB

Deux notebook jupyter :

	* Clound_mangodb : Prise en main des db non sql avec Mango atlas cloud 
	* Brief - mangodb - Projet Movies Database : Requêtes poussées de la manipulation d'une db non sql
	

Pour le Brief - mangodb - Projet Movies Database

### 1- Se connecter à la BDD Mflix

* Se connecter au serveur MongoDB de votre Atlas cluster

* Vérifier que les bases de données samples sont bien char* gées sur votre cluster Atlas : https://www.mongodb.com/docs/atlas/sample-data/

* Afficher les collections de la base de données : sample_mflix

* Afficher le nombre de documents par collection

### 2- Exploiter les données de Mflix

#### Part 1
* Afficher un document(quelconque) de la collection movies
* Combien ya t il de documents avec l'attribut year en string? et combien sont ils en int?
* Trouver un film avec "Salma Hayek" en tant qu'acteur
* Combien de films ou "Salma Hayek" a participé, afficher ces documents en se limitant au title et la liste des acteurs
* Afficher les 3 premiers films ou "Salma Hayek" a participé, afficher uniquement le title
* Combien de films nommés: "The Journey", la fonction find() retourne un objet itérable et non pas un document !
* Afficher pour chaque document :le titre, l'année et la liste des genres .

#### Part 2
* afficher les 12 titres de la collection movies à partir du dixième inclus ,
* afficher le résultat trié par ordre alphabétique décroissant
* Lister ts les films produits en 1979 ?
* Afficher les infos sur le film dont le title est "Alien" produit en 1979 ?
* Trouver ts les films qui ont gagné 100 awards ?
* Tous les films dont le titre commence par 'Re' ?
* Tous les films produits après 2010 et avant 2015 ?
* Afficher les films joués par l'acteur "Tom Cruise",sortis après l'année 2000, en se limitant au titre du film et la liste des acteurs ?
* Afficher tous les détails du film de "Tom Cruise",sorti en 2014, sauf son fullplot
* Chercher les films dans lesquels joue au moins un des acteurs suivants : Angelina Jolie,Brad Pitt
* Chercher les films dont on ne trouve aucun acteur de la liste suivante: Sandra Bullock,Tom Hanks,Julia Roberts,Kevin Spacey,George Clooney
* Lister les films parus en 2016 ou avec qui ont gagné 100 awards
* Lister les films parus après 2010 et dans lesquels l'un de ces acteurs a jouéSandra Bullock,Tom Hanks,Julia Roberts,Kevin Spacey,George Clooney
* Combien de films a comme director Clint Eastwood
* De la liste précédente et dans la collection comments de la BDD sample_mflix, combien de films ont été commentés
* Trouver la liste des films en doublons (meme titre) et combien d'occurences par titre

#### Part 3_Bonus
* Combien de films ont eu la note "PG-13" (indice : clé "rated") ? Afficher le 1er document ? Faire une projection dessus pour se limiter aux infos suivantes : _id, title, rated, year, writers et actors ? Afficher de nouveau ces dernières infos sans l'_id ?
* Trouver les films ayant la note "PG-13" et produits en 2009 ?
* Combien de films ont comme sous-clé "meter" de la clé "tomatoes" égale à 100 ?
* Combien de films dont "Jeff Bridges" a joué dedans ?
* idem mais "Jeff Bridges" se trouve ds la 1è position de l'array' "actors" ?
* Combien de films dont le "runtime" est sup ou égale à 90 min ET inf ou égale à 120 min ?
* Combien de films dont le meter de la clé tomatoes est sup à 95 OU le "metacritic" est sup à 88 ?
* Combien de films dont lemeter de la clé tomatoes est sup ou égale à 95 min ET le "runtime" est sup à 180 min
* Combien de films dont la clé "tomatoes.viewer.meter" n'est pas égale à "blabla" ?
* Combien de films dont la clé "tomato.meter" existe (et inversement) ?
* modifier dans le document ayant le title : Blacksmith Scene , la valeur de l'attribut movie à "blabla"
* Combien de films ont été écrit par ""Ethan Coen" et "Joel Coen"" ?
* Combien de films ont été écrit par "Joel Coen" et "Ethan Coen" ? est ce que l'ordre est important
* Combien de film ont été produit par un seul pays ?
* Combien de film dont la clé genre est un tableau qui contient Comedy, Crime et Drame ?
* Combien de films dont parmi les auteurs on trouve "Ethan Coen" et "Joel Coen" (resp. "Ethan Coen" ou "Joel Coen") ?
* Combien de films ont engendré des recettes sup à 5M£ en UK


#### Part 4 Bonus:
Réfléchir à un schéma qui représente la BDD sample_mflix (avec ttes ses collections)


#### Bonus (Module 1+ Module 3)
On considère la collection movies as a dataset, essayer de construire un dataframe avec ces données.

1- Preporcessing: Faire un état des lieux sur ce jeu de données: nombre de valeurs manquantes, nombre de valeur nulles, vérifier les doublons.., Nettoyer les données avec des anomalies(s'il y en a )..

2- DataViz: faire une analyse exploratoire (top 10 des acteurs les plus presents dans les films,nombre de films par année..)