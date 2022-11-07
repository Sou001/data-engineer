import pyspark.sql.functions as F
from spark_cities.models.cities import Cities
from spark_cities.geospatial import split_lat_long


def main(spark):
  df_cities = Cities.read(spark) #lire en utilisant la class Cities de model

  # ecrire en utilisant la class Cities de models
  Cities.write(df_cities)
