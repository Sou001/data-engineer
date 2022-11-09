
from spark_cities.models.cities import Cities
from pyspark.sql.types import StringType

def test_split_lat_long(spark_session):
    # GIVEN

    cities = Cities(spark_session)

    cities_infos = ["46.999873398,6.498147193", "47.361512085,6.235167025", ""]

    input_df = spark_session.createDataFrame(cities_infos, StringType()).toDF(*["coordonnees_gps"]) 
    # create df with spark_session

    # WHEN
    actual_df = cities.split_lat_long(input_df)
    
    actual = [x.asDict() for x in actual_df.collect()] #transformer actual_df en une list de dictionaire

    # THEN
    expected = [
      {"latitude": 46.999873398, "longitude": 6.498147193},
      {"latitude": 47.361512085, "longitude": 6.235167025},
      {"latitude": None, "longitude": None}
    ]
    assert actual == expected #verify equality between the two

def test_departement(spark_session):
    # GIVEN

    cities = Cities(spark_session)

    cities_infos = ["25650", "68640", ""]

    input_df = spark_session.createDataFrame(cities_infos, StringType()).toDF(*["code_postal"])
    # create df with spark_session

    # WHEN
    actual_df = cities.departement(input_df)
    actual = [x.asDict() for x in actual_df.collect()] 
        # transformer actual_df en une list de dictionaire

    # THEN
    expected = [
      {"code_postal": "25650", "dept": "25"},
      {"code_postal": "68640", "dept": "68"},
      {"code_postal": "", "dept": ""}
    ]
    assert actual == expected # verify equality between the two
