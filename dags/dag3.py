from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pymysql
from hdfs import InsecureClient

def transform_and_save_to_hadoop():
    # Conectar ao MySQL
    mysql_conn = pymysql.connect(
        host='mysql',
        user='root',
        password='fiapOn', # Aspas corrigidas
        database='dbfiapon'
    )
    
    # Conectar ao HDFS
    hdfs_client = InsecureClient('http://hadoop:9870', user='hadoop')

    try:
        with mysql_conn.cursor() as cursor:
            # Query para a tabela 3
            cursor.execute("SELECT * FROM tabela3")
            data = cursor.fetchall()

            # Transformação (ID, Valor)
            transformed_data = [f"{item[0]}, {item[1]}" for item in data]

            # Salvar no HDFS
            hdfs_path = '/user/hadoop/tabela3_output.txt'
            with hdfs_client.write(hdfs_path, encoding='utf-8', overwrite=True) as writer:
                for line in transformed_data:
                    writer.write(line + '\n')
    finally:
        mysql_conn.close()

# Definição da DAG
with DAG(
    dag_id='dag3', 
    start_date=datetime(2023, 1, 1), 
    schedule_interval='@daily',
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id='transform_and_save_to_hadoop_t3', 
        python_callable=transform_and_save_to_hadoop
    )

    task1