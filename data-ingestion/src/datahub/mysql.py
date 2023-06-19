from pyspark.sql import SparkSession
from sqlalchemy import create_engine

def check_from_table(table_name):
    # Create a SparkSession
    spark = SparkSession.builder \
        .appName("Read from Table") \
        .getOrCreate()
    db_url = "mysql+pymysql://root:'Password@123'@localhost:3306/nuodata"
    engine = create_engine(db_url)
    # Read from the table
    table_df = spark.read.format("jdbc") \
        .option("url", db_url) \
        .option("dbtable", table_name) \
        .load()

    # Show the DataFrame
    table_df.show()