import os
import shutil

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from pendulum import timezone
from airflow.exceptions import AirflowException
from airflow.models import TaskInstance


default_args = {
    'owner': 'arthur bissa',
    'retries':2,
    'retry_delay': timedelta(minutes=2)
}


def step2_start():
    print("step2 is starting now")
    

def folder_creation(**context):
    current_date = context['ds']

    context['ti'].xcom_push(key='date',value=current_date)

    base_dir = "/home/anorakbs"

    data_dir = os.path.join(base_dir,'data') 

    csv_folder_path = os.path.join(data_dir, 'csv', current_date)
    os.makedirs(csv_folder_path, exist_ok=True) 

    tables_list = [ "categories",
                    "customer_customer_demo",
                    "customer_demographics",
                    "customers",
                    "employee_territories",
                    "employees",
                    "orders",
                    "products",
                    "region",
                    "shippers",
                    "suppliers",
                    "territories",
                    "us_states"
                ]
    
    for tables in tables_list:
        tables_folder = os.path.join(data_dir,'postgres',tables,current_date)
        os.makedirs(tables_folder, exist_ok=True)

def rename_csv_files(**context):
    current_date = context['ds']

    base_dir = "/home/anorakbs"
    
    data_dir = os.path.join(base_dir,'data')

    csv_folder_path = os.path.join(data_dir, 'postgres', 'orders',current_date)

    for filename in os.listdir(csv_folder_path):
        if filename.endswith(".csv"):
            new_name = "orders.csv"
            os.rename(os.path.join(csv_folder_path, filename), os.path.join(csv_folder_path, new_name))
            print(f"Renamed {filename} to {new_name}")

with DAG(
    default_args=default_args,
    dag_id= 'dag_pipeline_indicium',
    description= 'DAG using python operator to copy the csv to my local machine',
    start_date= datetime(2024,2,8,21,25,tzinfo=timezone('America/Belem')),
    schedule_interval='25 21 * * *'
) as dag:
    
    task1 = PythonOperator(
        task_id= 'folder_creation',
        python_callable=folder_creation,
        provide_context=True
    )

    task2 = BashOperator(
        task_id='meltano_copy',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano config target-csv set destination_path ../data/csv/{{task_instance.xcom_pull(task_ids='folder_creation',key='date')}} && "
                      "meltano run tap-csv target-csv"
                      )

    )

    task3 = BashOperator(
        task_id='meltano_extractor_categories',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano config target-csv-categories set destination_path ../data/postgres/categories/{{task_instance.xcom_pull(task_ids='folder_creation',key='date')}} && "
                      "meltano run tap-postgres-categories target-csv-categories"
                      )

    )

    task4 = BashOperator(
        task_id='meltano_extractor_customer_customer_demo',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano config target-csv-customer_customer_demo set destination_path ../data/postgres/customer_customer_demo/{{task_instance.xcom_pull(task_ids='folder_creation',key='date')}} && "
                      "meltano run tap-postgres-customer_customer_demo target-csv-customer_customer_demo"
                      )

    )

    task5 = BashOperator(
        task_id='meltano_extractor_customer_demographics',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano config target-csv-customer_demographics set destination_path ../data/postgres/customer_demographics/{{task_instance.xcom_pull(task_ids='folder_creation',key='date')}} && "
                      "meltano run tap-postgres-customer_demographics target-csv-customer_demographics"
                      )

    )
    task6 = BashOperator(
        task_id='meltano_extractor_customers',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano config target-csv-customers set destination_path ../data/postgres/customers/{{task_instance.xcom_pull(task_ids='folder_creation',key='date')}} && "
                      "meltano run tap-postgres-customers target-csv-customers"
                      )

    )
    task7 = BashOperator(
        task_id='meltano_extractor_employee_territories',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano config target-csv-employee_territories set destination_path ../data/postgres/employee_territories/{{task_instance.xcom_pull(task_ids='folder_creation',key='date')}} && "
                      "meltano run tap-postgres-employee_territories target-csv-employee_territories"
                      )

    )
    task8 = BashOperator(
        task_id='meltano_extractor_employees',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano config target-csv-employees set destination_path ../data/postgres/employees/{{task_instance.xcom_pull(task_ids='folder_creation',key='date')}} && "
                      "meltano run tap-postgres-employees target-csv-employees"
                      )

    )
    task9 = BashOperator(
        task_id='meltano_extractor_orders',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano config target-csv-orders set destination_path ../data/postgres/orders/{{task_instance.xcom_pull(task_ids='folder_creation',key='date')}} && "
                      "meltano run tap-postgres-orders target-csv-orders"
                      )

    )
    task10 = BashOperator(
        task_id='meltano_extractor_products',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano config target-csv-products set destination_path ../data/postgres/products/{{task_instance.xcom_pull(task_ids='folder_creation',key='date')}} && "
                      "meltano run tap-postgres-products target-csv-products"
                      )

    )
    task11 = BashOperator(
        task_id='meltano_extractor_region',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano config target-csv-region set destination_path ../data/postgres/region/{{task_instance.xcom_pull(task_ids='folder_creation',key='date')}} && "
                      "meltano run tap-postgres-region target-csv-region"
                      )

    )
    task12 = BashOperator(
        task_id='meltano_extractor_shippers',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano config target-csv-shippers set destination_path ../data/postgres/shippers/{{task_instance.xcom_pull(task_ids='folder_creation',key='date')}} && "
                      "meltano run tap-postgres-shippers target-csv-shippers"
                      )

    )
    task13 = BashOperator(
        task_id='meltano_extractor_suppliers',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano config target-csv-suppliers set destination_path ../data/postgres/suppliers/{{task_instance.xcom_pull(task_ids='folder_creation',key='date')}} && "
                      "meltano run tap-postgres-suppliers target-csv-suppliers"
                      )

    )
    task14 = BashOperator(
        task_id='meltano_extractor_territories',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano config target-csv-territories set destination_path ../data/postgres/territories/{{task_instance.xcom_pull(task_ids='folder_creation',key='date')}} && "
                      "meltano run tap-postgres-territories target-csv-territories"
                      )

    )
    task15 = BashOperator(
        task_id='meltano_extractor_us_states',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano config target-csv-us_states set destination_path ../data/postgres/us_states/{{task_instance.xcom_pull(task_ids='folder_creation',key='date')}} && "
                      "meltano run tap-postgres-us_states target-csv-us_states"
                      )

    )
    
    task16 = PythonOperator(
        task_id='step_2_start',
        python_callable=step2_start,
        trigger_rule='none_failed'
    )
    
    task17 = BashOperator(
        task_id='meltano_load_order_details',
        bash_command=("cd .. & cd /home/anorakbs && ls && "
                      "source meltano_teste/bin/activate && "
                      "cd meltano-project && "
                      "meltano run tap-csv target-postgres-final"
                      )

    )

    task18 = PythonOperator(
        task_id='rename_csv_files',
        python_callable=rename_csv_files,
    )


    task19 = BashOperator(
    task_id='meltano_load_orders',
    bash_command=(
        "cd .. && cd /home/anorakbs && ls &&"
        "source meltano_teste/bin/activate && "
        "cd meltano-project && "
        "meltano config tap-csv-orders set files "
        "'[{\"entity\": \"orders\", \"path\": \"../data/postgres/orders/{{ task_instance.xcom_pull(task_ids='folder_creation', key='date') }}/orders.csv\", "
        "\"delimiter\": \",\", \"keys\": [\"order_id\", \"customer_id\", \"employee_id\", \"order_date\", \"required_date\", \"shipped_date\", \"ship_via\", \"freight\", \"ship_name\", \"ship_address\", \"ship_city\", \"ship_region\", \"ship_postal_code\", \"ship_country\"]}]' && "
        "meltano run tap-csv-orders target-postgres-final"

    )
)


    task1 >> task2 >> [task3,task4,task5,task6,task7,task8,task9,task10,task11,task12,task13,task14,task15] >> task16 >> task17 >> task18 >> task19

    