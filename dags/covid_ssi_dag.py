from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
# from airflow.models import Variable
import os

from src.extract import download_files, unzip_csv_file
from src.transform import process_ssi_data

default_args = {
    'owner': 'biogitte',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 14),
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
}

with DAG('capture_data_dag', default_args=default_args, schedule_interval='@daily') as dag:
    # Set variables
    RAW_DIR = os.getenv('RAW_DIR')

    capture_data_task = PythonOperator(
        task_id='capture_data_task',
        python_callable=download_files,
        op_kwargs={
            'url_dict': {
                "https://raw.githubusercontent.com/mok0/covid19-data-denmark/master/covid19-data-denmark.csv": "ssi_covid_dk",
                "https://raw.githubusercontent.com/mok0/covid19-data-denmark/master/cases_vs_age.csv": "ssi_cases_by_age_dk",
                "https://raw.githubusercontent.com/mok0/covid19-data-denmark/master/mutant_data.csv": "ssi_mutations_dk",
                "https://raw.githubusercontent.com/mok0/covid19-data-denmark/master/vaccinations.csv": "ssi_vaccinations_dk",

            },
            'destination': RAW_DIR
        }

    )

    extract_data_task = PythonOperator(
        task_id='extract_data_task',
        python_callable=unzip_csv_file,
        op_kwargs={
            'url': "https://files.ssi.dk/covid19/spildevand/data/data-spildevand-sarscov2-uge23-2023-alof",
            'destination': RAW_DIR
                   }
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=process_ssi_data,
        op_kwargs={'file_paths': {
            "ssi_covid_dk_path": f"{RAW_DIR}/*ssi_covid_dk*",
            "ssi_cases_by_age_dk_path": f"{RAW_DIR}/*ssi_cases_by_age_dk*",
            "ssi_mutations_dk_path": f"{RAW_DIR}/*ssi_mutations_dk*",
            "ssi_vaccinations_dk_path": f"{RAW_DIR}/*ssi_vaccinations_dk*",
            "ssi_spildevand_dk_path": f"{RAW_DIR}/*dk_spildevandsdata*"}
        },
    )

    capture_data_task >> extract_data_task >> transform_task
