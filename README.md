# Building Data Lakehouse

This project is designed to construct a data lakehouse. This data lakehouse will enable organizations to store, manage, and analyze large datasets in a cost-effective, secure, and scalable manner. The data lakehouse will provide a centralized repository for all data, allowing users to easily access and query the data with a unified interface.

Minio will provide distributed object storage to store the data, Delta Lake will provide ACID-compliant transactions for managing the data, Spark will enable distributed computing for analytics, Presto will provide fast SQL queries, and Hive Metastore will provide a unified catalog for the data. This data lakehouse will enable organizations to quickly and easily access and analyze valuable data, allowing them to make better data-driven decisions.

This project aims also to create an Extract, Load, and Transform (ELT) pipeline to ingest data from a Postgres database into our lakehouse. The ELT pipeline will make use of Apache Spark, to extract the data from the Postgres database, load it into the lakehouse, and then transform it into the desired format. Once the data is loaded into the lakehouse, it will be available for downstream analytics and reporting.
## Architecture

![Architecture](/images/1.png "Architecture")


## Setup
- First, build Spark and Presto docker image
```bash
docker build -t presto:0.272.1 ./Dockerfiles/presto
docker build -t cluster-apache-spark:3.1.1 Dockerfiles/spark
```
- Run docker compose
```bash
docker-compose up
```

- Create a bucket in [minio](http://localhost:9001) to store our data (name it datalake)

- Create a Postgres database (name it CarParts and use CarParts.sql file to create tables)
- Install jar files needed for our spark project
```bash
docker exec -it master bash /opt/workspace/dependencies/packages_installer.sh 
```
- Run the first script
```bash
docker exec -it master spark-submit --master spark://master:7077 \
        --deploy-mode cluster \
        --executor-memory 5G \
        --executor-cores 8 \
        /opt/workspace/postgres_to_s3.py
```

- Run the second script
```bash
docker exec -it master spark-submit --master spark://master:7077 \
        --deploy-mode cluster \
        --executor-memory 5G \
        --executor-cores 8 \
        /opt/workspace/clean_data.py
```
## links
- **Spark master UI:**    http://localhost:9090
- **Spark worker a UI:**  http://localhost:9091
- **Spark worker b UI:**  http://localhost:9092
- **Minio:**  http://localhost:9001
- **Presto:** http://localhost:8000

## Built With

- Spark
- Minio
- PostgreSQL
- Hive Metastore
- Presto
- Delta Lake


## Author

**Youssef EL ASERY**

- [Profile](https://github.com/ysfesr "Youssef ELASERY")
- [Linkedin](https://www.linkedin.com/in/youssef-elasery/ "Welcome")
- [Kaggle](https://www.kaggle.com/youssefelasery "Welcome")


## 🤝 Support

Contributions, issues, and feature requests are welcome!

Give a ⭐️ if you like this project!
