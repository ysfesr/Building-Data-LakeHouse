import os
from pyspark.sql import SparkSession
from datetime import date

today = date.today().strftime("%b-%d-%Y")

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_S3_ENDPOINT = os.getenv("AWS_S3_ENDPOINT")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
HIVE_METASTORE_URI = os.getenv("HIVE_METASTORE_URI")

spark = SparkSession.builder \
    .appName('Clean data') \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083")\
    .config("spark.sql.warehouse.dir","s3a://datalake/warehouse")\
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
    .enableHiveSupport()\
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

spark.sql("CREATE DATABASE IF NOT EXISTS dwh COMMENT 'Data Warehouse for Car Part'")


# Reading tables from landing area
print('\nReading ...')
Brand = spark.read.format("delta").load(f's3a://datalake/bronze/CarPartsDB/{today}/Brand')
Car = spark.read.format("delta").load(f's3a://datalake/bronze/CarPartsDB/{today}/Car')
Customer = spark.read.format("delta").load(f's3a://datalake/bronze/CarPartsDB/{today}/Customer')
Orders = spark.read.format("delta").load(f's3a://datalake/bronze/CarPartsDB/{today}/Orders')
Part_for_Car = spark.read.format("delta").load(f's3a://datalake/bronze/CarPartsDB/{today}/Part_for_Car')
Part_in_Order = spark.read.format("delta").load(f's3a://datalake/bronze/CarPartsDB/{today}/Part_in_Order')
Part_Maker = spark.read.format("delta").load(f's3a://datalake/bronze/CarPartsDB/{today}/Part_Maker')
Part_Supplier = spark.read.format("delta").load(f's3a://datalake/bronze/CarPartsDB/{today}/Part_Supplier')
Part = spark.read.format("delta").load(f's3a://datalake/bronze/CarPartsDB/{today}/Part')
Supplier = spark.read.format("delta").load(f's3a://datalake/bronze/CarPartsDB/{today}/Supplier')
print('End of reading... \n')



# transforming tables to a set of dimensionel tables
print('\ntransforming ...')
Brand.write.format('delta').mode('overwrite').option('path','s3a://datalake/silver/warehouse/CarParts/Dim_Brand').saveAsTable("dwh.DimBrand")
Car.write.format('delta').mode('overwrite').option('path','s3a://datalake/silver/warehouse/CarParts/Dim_Car').saveAsTable("dwh.DimCar")
Customer.write.format('delta').mode('overwrite').option('path','s3a://datalake/silver/warehouse/CarParts/Dim_Customer').saveAsTable("dwh.DimCustomer")
Orders.write.format('delta').mode('overwrite').option('path','s3a://datalake/silver/warehouse/CarParts/Dim_Orders').saveAsTable("dwh.DimOrders")
Part_Maker.write.format('delta').mode('overwrite').option('path','s3a://datalake/silver/warehouse/CarParts/Dim_Part_Maker').saveAsTable("dwh.DimPartMaker")
Part_for_Car.write.format('delta').mode('overwrite').option('path','s3a://datalake/silver/warehouse/CarParts/Dim_Part_for_Car').saveAsTable("dwh.DimPartForCar")
Part_Supplier.write.format('delta').mode('overwrite').option('path','s3a://datalake/silver/warehouse/CarParts/Dim_Part_Supplier').saveAsTable("dwh.DimPartSupplier")
Supplier.write.format('delta').mode('overwrite').option('path','s3a://datalake/silver/warehouse/CarParts/Dim_Supplier').saveAsTable("dwh.DimSupplier")
Part.write.format('delta').mode('overwrite').option('path','s3a://datalake/silver/warehouse/CarParts/Dim_Part').saveAsTable("dwh.DimPart")

Part_in_Order.join(Orders, 'order_id') \
    .join(Part_Supplier,'part_supplier_id')\
    .join(Part, 'part_id')\
    .join(Part_for_Car, 'part_id')\
    .join(Car, 'car_id')\
    .select("part_in_order_id", "brand_id", "car_id", "car_manufacturer_id", "customer_id", "order_id", "part_id",
       "part_maker_id", "part_supplier_id", Part.supplier_id, "actual_sale_price", "quantity")\
    .write.format('delta').mode('overwrite')\
    .option('path','s3a://datalake/silver/warehouse/CarParts/Fact_part_in_Order').saveAsTable("dwh.FactPartInOrder")
print('End Of Transforming')