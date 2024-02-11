
# Indicium Tech Code Challenge

This project demonstrates an automated data pipeline using Airflow, Meltano, and Docker. It showcases the extraction, transformation, and loading (ETL) process of data from various sources into a PostgreSQL database.

## Disclaimer

This pipeline has been developed and tested using WSL for Windows. Adaptations may be necessary for other environments.

## Overview

The project employs Airflow for workflow orchestration, Meltano for ETL operations, and Docker to containerize the PostgreSQL database. It includes custom taps and targets with Meltano for data extraction and loading, and Airflow to manage the pipeline's execution.

## Installation

### Setup Virtual Environments

1. **Create virtual environments for Airflow and Meltano:**

```bash
virtualenv airflow_env
virtualenv meltano_env
```

2. **Activate the Airflow virtual environment and set up Airflow:**

```bash
source airflow_env/bin/activate
pip install "apache-airflow[celery]==2.8.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.8.txt"
airflow db init
airflow users create --username airflow --firstname airflow --lastname airflow --role Admin --email your_email@example.com --password airflow
```

3. **Start the Airflow webserver and scheduler:**

```bash
airflow webserver --port 8080
airflow scheduler
```

4. **Activate the Meltano virtual environment and install Meltano:**

```bash
source meltano_env/bin/activate
pip install meltano
meltano init meltano-project
```

### Install Plugins with Meltano

```bash
meltano add extractor tap-csv
meltano add extractor tap-postgres
meltano add loader target-postgres
meltano add loader target-csv
meltano add mapper meltano-map-transformer
```

### Initialize Database

In the root directory, start the PostgreSQL database using Docker:

```bash
docker-compose up
```

## Pipeline Overview

The pipeline consists of several stages, including data preparation, extraction, transformation, and loading. The process begins with a Python operator creating necessary folders and passing dates to other tasks, which then extract data from CSV and PostgreSQL sources and load it into a final PostgreSQL database.

![pipeline image](https://github.com/AnorakBs/code-challenge-indicium/blob/main/images/Screenshot_1.png)

![pipeline image](https://github.com/AnorakBs/code-challenge-indicium/blob/main/images/Screenshot_4.png)

First, I have the Python operator that will create the folders, and also pass the date to my other tasks.

After that, it's the extraction of the data and saving it in the local filesystem.

The first extraction is a copy of the order details from one place to another.
After that, I will have the extractions of the tables in the PostgreSQL database.

### Data Extraction and Loading

Extractions are performed using custom Meltano taps and targets, with Bash operators executing Meltano commands for each task.

After all extractions are completed, there's a task that will initiate step 2 of the pipeline.

It will only initiate if all other tasks before itself are successful.

The next task is loading the CSV of the order_details into our final database.

Following this task, I have a task that will rename one of the CSV files that we have extracted from the table. This task can be replicated to make all the files have the same name. I only have made this work for the CSV orders to later show my results.

## Final Database

The final database has been created in the same PostgreSQL instance that is running on Docker.

### Pipeline Execution

The DAG configuration enables running tasks for past dates, facilitating backfills or reprocessing of historical data.

## Querying Results

The final part of the pipeline demonstrates querying the PostgreSQL database, joining tables to showcase the end results of the ETL process.

![pipeline image](https://github.com/AnorakBs/code-challenge-indicium/blob/main/images/Screenshot_3.png)

## Challenges Encountered

In this challenge, I have run into a few problems, haha.

Particularly with the lack of Meltano examples and the initial usage of Airflow.

I had never used Meltano before, so I had to really try to understand the documentation, and boy, that was a real challenge.

I also tried using docker for airflow and meltano but could make the services talk with each other, that's the reason that i chose to use WSL.

The main reason that I used bash operator for all Meltano tasks was because I just couldn't install the Airflow utility plugin, and I tried a lot. Another issue using Meltano was in the extraction part. It took me quite a while to make it work. I don't know if what I did was the best thing, but it works.

This was one of my first times using Airflow too. It was fun; for the future, I will invest more time in learning this tool.



## Adaptation for Other Environments

While this pipeline was developed in a WSL environment, modifications may be necessary for other systems, especially regarding path configurations for Meltano and Airflow setups.

