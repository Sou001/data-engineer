from pyspark.sql import functions as F

def split_lat_long(df, lat_long_col):
  return df.withColumn("latitude", F.col(lat_long_col) ) 
  # extraire la latitude et la longitude à partir de la column lat_long_col
