from pyspark.sql import SparkSession
from spark_cities.main import main

if __name__ == "__main__":
  # init spark session
  spark = SparkSession.builder.appName("spark_cities").getOrCreate()
  spark.sparkContext.setLogLevel("WARN")

  # launch spark of spark-cities app
  main(spark)
  
  #spark.sparkContext.stop()
