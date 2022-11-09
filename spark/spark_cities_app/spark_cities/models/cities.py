
## Pyspark libs
from pyspark.sql import functions as F
from pyspark.sql.functions import col, split, substring, udf, when, lit
from pyspark.sql.types import StringType, DoubleType, IntegerType
from pyspark.sql import Window
from geopy.distance import geodesic

## Python libs for dist calc
from math import sin, cos, sqrt, atan2, radians


class Cities:

  def __init__(self, spark):
    
    self.spark = spark

    self.coordonnees_gps = "coordonnees_gps"
    self.code_commune_insee = "code_commune_insee"
    self.nom_de_la_commune = "nom_de_la_commune"
    self.code_postal = "code_postal"
    self.ligne_5 = "ligne_5"
    self.libelle_d_acheminement = "libelle_d_acheminement"

    self.dist_udf = udf(Cities.calc_dist,DoubleType())
    self.geopy_udf = udf(Cities.geopy_dist,DoubleType())
  

  def read(self):
    return self.spark.read.csv("hdfs://localhost:9000/data/raw/cities/v1/csv", header=True, sep=";") 
    # lecture csv in hdfs avec header=Treu sep=";"

  def write(self, df, save_format, options, chemin):
    # ecriture parquet
    df.write.format(save_format).options(**options).mode('overwrite').save(chemin)

  def departement(self, df):
    return df.withColumn("dept",substring(col(self.code_postal),1,2).cast(StringType()))

  def departement_udf(self, df):
    udf_dept = udf(lambda s: s[:2] if s[:2]!="20" else "2A" if (int(s)<20200) else "2B", StringType())
    return df.withColumn("dept", udf_dept(col(self.code_postal)))
    
  def departement_fct(self, df):
    return  df.withColumn("dept", when(( (substring(col(self.code_postal), 1,2)=="20") & 
                                      (col(self.code_postal).cast(IntegerType()) < 20200)
                                    ), lit("2A"))\
                              .when(((substring(col(self.code_postal), 1,2)=="20") & 
                                     (col(self.code_postal).cast(IntegerType()) >= 20200 )), 
                                     lit("2B"))\
                              .otherwise(substring(col(self.code_postal),1,2).cast(StringType()))
                      )

  def split_lat_long(self, df):
    return df.withColumn("latitude", split(col(self.coordonnees_gps),',')[0].cast(DoubleType()))\
             .withColumn("longitude", split(col(self.coordonnees_gps),',')[1].cast(DoubleType()))\
             .drop(self.coordonnees_gps)

  def nb_com_per_dept(self, df):
    return df.select("dept","code_commune_insee")\
              .dropDuplicates()\
              .groupBy("dept")\
              .count()\
              .withColumnRenamed("count","nombre_commune")\
              .orderBy(col("nombre_commune").desc())
  
  ## Fonction qui servira a calculer la distance avec les infos sur latitude et longitude
  @staticmethod
  def calc_dist(lat1,lon1,lat2,lon2) :
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

  def pref_coordonnees_gps(self, df):

    window = Window.partitionBy("dept")
    magic_percentile = F.expr('percentile_approx(dist_perf, 0.5)')

    df = self.split_lat_long(df)\
             .withColumn(self.code_postal, col(self.code_postal).cast(IntegerType()))\
             .where((col("longitude").isNotNull() & col("latitude").isNotNull()))

    return df.withColumn("min_code_postale", F.min(col(self.code_postal)).over(window))\
             .join(df.select(col(self.code_postal).alias("min_code_postale"),
                             col("latitude").alias("latitude1"),
                             col("longitude").alias("longitude1"))\
                     .dropDuplicates(), 'min_code_postale', "inner")\
             .drop("min_code_postale")\
             .withColumn("dist_perf", self.dist_udf(col("latitude"),col("longitude"),
                                                    col("latitude1"),col("longitude1")))\
             .select("dept","dist_perf")\
             .withColumn("mean_dist", F.mean("dist_perf").over(window).cast(DoubleType()))\
             .withColumn("median_dist", magic_percentile.over(window).cast(DoubleType()))\
             .drop("dist_perf")\
             .dropDuplicates()

  
  def geopy_dist(a,b):
    return geodesic([float(x) for x in a.split(",")], [float(x) for x in b.split(",")]).km

  def pref_coordonnees_gps_v2(self, df):

    window = Window.partitionBy("dept")
    magic_percentile = F.expr('percentile_approx(dist_perf, 0.5)')

    df = df.withColumn(self.code_postal, col(self.code_postal).cast(IntegerType()))\
           .where((col(self.coordonnees_gps).isNotNull()))

    return df.withColumn("min_code_postale", F.min(col(self.code_postal)).over(window))\
             .join(df.select(col(self.code_postal).alias("min_code_postale"),
                             col(self.coordonnees_gps).alias("coordonnees_gps1"))\
                     .dropDuplicates(), 'min_code_postale', "inner")\
             .drop("min_code_postale")\
             .withColumn("dist_perf", self.geopy_udf(col("coordonnees_gps"),col("coordonnees_gps1")))\
             .select("dept","dist_perf")\
             .withColumn("mean_dist", F.mean("dist_perf").over(window).cast(DoubleType()))\
             .withColumn("median_dist", magic_percentile.over(window).cast(DoubleType()))\
             .drop("dist_perf")\
             .dropDuplicates()

      