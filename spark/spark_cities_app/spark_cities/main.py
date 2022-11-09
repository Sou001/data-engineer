
from spark_cities.models.cities import Cities
import time

def main(spark):

  cities = Cities(spark)

  ## Partie APP
  df_cities = cities.read()\
                    .persist() #lire en utilisant la class Cities de model

  # ecrire en utilisant la class Cities de models
  cities.write(df_cities, 'parquet', {}, '/data/experiment/cities/v1/parquet')

  ## Partie Manipulation de base
    # clean_cities - select columns and create new one depending on code_postal
  df_clean_cities = cities.departement(df_cities.select("code_commune_insee","nom_de_la_commune",
                                                        "code_postal","coordonnees_gps"))\
                          .persist()
    # write clean cities
  cities.write(df_clean_cities, 'parquet', {}, '/data/refined/cities/v1/parquet')

  ## Partie test
    # On split la colonne coordonnees_gps et on va apres creer la colonne dept
    # same as df_cities without coord gps and 3 new cols : lat, long and dept
  cities.write(cities.departement(cities.split_lat_long(df_cities)),
               'parquet',
               {},
               '/data/refined/cities/v1/parquet')
  
  ## Partie Jointure et aggregation
    # tab 2 colonnes : dept, nb_commune
  cities.write(cities.nb_com_per_dept(df_clean_cities), 
               'csv',
               {'delimiter':";"},
               '/data/refined/departement/v1/csv')

  ## Partie UDF

    # udf departement v2 - extraction dept avec udf
  start = time.time()
  df_udf_dept = cities.departement_udf(df_cities).persist()
  end = time.time()

  print("elapsed time on udf : " + str(end - start))

  cities.write(df_udf_dept,
               'csv',
               {'delimiter':";"},
               '/data/refined/departement/v2/csv')

    # cas corse
  start = time.time()
  cities.departement_fct(df_cities)
  end = time.time()

  print("elapsed time on fct dept  : " + str(end - start))

  ## Partie Window
    # A chaque ville ajouter les coordonnees GPS de la prefecture du departement
		# La prefecture du departement se situe dans la ville ayant le code postal le plus petit 
    # dans tout le departement.

  # version 1 avec udf et fonction python - maths 
  cities.write(cities.pref_coordonnees_gps(df_udf_dept),
               'csv',
               {'delimiter':";"},
               '/data/refined/departement/v3/csv')

  # version 2 avec geopy et passage de l env python cree dans spark submit
  cities.write(cities.pref_coordonnees_gps_v2(df_udf_dept),
               'csv',
               {'delimiter':";"},
               '/data/refined/departement/v4/csv')
  
  ## Closure step : unpersist tables
  df_cities.unpersist()
  df_clean_cities.unpersist()
  df_udf_dept.unpersist()