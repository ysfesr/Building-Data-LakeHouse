# Building Data Lakehouse

Building of a data lakehouse and a data pipeline

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
