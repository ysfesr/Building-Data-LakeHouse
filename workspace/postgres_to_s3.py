import os
from pyspark.sql import SparkSession
from datetime import date

today = date.today().strftime("%b-%d-%Y")


AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_S3_ENDPOINT = os.getenv("AWS_S3_ENDPOINT")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_ENDPOINT = os.getenv("POSTGRES_ENDPOINT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

spark = SparkSession.builder \
    .appName('Postgres to S3 pipeline') \
    .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY) \
    .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_KEY) \
    .config("fs.s3a.endpoint", AWS_S3_ENDPOINT)\
    .config("spark.hadoop.fs.s3a.path.style.access", "true")\
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("fs.s3a.connection.ssl.enabled", "false")\
    .config('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
    .config('spark.jars','/opt/spark/jars/aws-java-sdk-bundle-1.11.375.jar')\
    .config('spark.jars','/opt/spark/jars/hadoop-aws-3.2.0.jar')\
    .config('spark.jars','/opt/spark/jars/delta-core_2.12-1.0.1.jar')\
    .config('spark.jars','/opt/spark/jars/postgresql-42.3.5.jar')\
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

tables_names = ['Part_in_Order', 'Supplier', 'Brand', 'Part', 'Part_for_Car', 'Part_Supplier', \
               'Customer', 'Customer_Statut', 'Orders', 'Car_Manufacturer', 'Car', 'Part_Maker']

postgres_url= f"jdbc:postgresql://{POSTGRES_ENDPOINT}/{POSTGRES_DB}"

for table_name in tables_names:
    print(f"{table_name} table transformation ...")

    spark.read \
    .format("jdbc") \
    .option("url", postgres_url) \
    .option("dbtable", table_name) \
    .option("user", POSTGRES_USER) \
    .option("password", POSTGRES_PASSWORD) \
    .option("driver", "org.postgresql.Driver") \
    .load() \
    .write \
    .format("delta")\
    .mode("overwrite")\
    .save(f"s3a://{AWS_BUCKET_NAME}/bronze/CarPartsDB/{today}/{table_name}")
    print(f"{table_name} table done!")