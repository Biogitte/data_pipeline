import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from src.file_downloader import download_files

url_dict = {
            "https://raw.githubusercontent.com/mok0/covid19-data-denmark/master/covid19-data-denmark.csv": "ssi_covid_dk",
            "https://raw.githubusercontent.com/mok0/covid19-data-denmark/master/cases_vs_age.csv": "ssi_cases_by_age_dk",
            "https://raw.githubusercontent.com/mok0/covid19-data-denmark/master/mutant_data.csv": "ssi_mutations_dk",
            "https://raw.githubusercontent.com/mok0/covid19-data-denmark/master/vaccinations.csv": "ssi_vaccinations_dk",
            "https://files.ssi.dk/covid19/spildevand/data/data-spildevand-sarscov2-uge23-2023-alof": "",
        }

default_args = {
    'owner': 'biogitte',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 14),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG('capture_data_dag', default_args=default_args, schedule_interval='@daily') as dag:

    def download_data():
        destination = os.getenv('RAW_DIR')
        download_files(destination=destination, url_dict=url_dict)

    capture_data_task = PythonOperator(
        task_id='capture_data_task',
        python_callable=download_data,
    )

    capture_data_task
