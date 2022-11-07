class Cities:

  COORDONNEES_GPS = "coordonnees_gps"
  code_commune_insee = "code_commune_insee"
  nom_de_la_commune = "nom_de_la_commune"
  code_postal = "code_postal"
  ligne_5 = "ligne_5"
  libelle_d_acheminement = "libelle_d_acheminement"
  
  @staticmethod
  def read(spark):
    return spark.read.csv("hdfs://localhost:9000/data/raw/cities/v1/csv",header=True,sep=";") # change into hdfs lecture csv avec header=Treu sep=";"

  @staticmethod
  def write(df):
    # ecriture parquet
    df.write.format('parquet').mode('overwrite').parquet('/data/experiment/cities/v1/parquet')
