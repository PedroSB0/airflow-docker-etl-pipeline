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
        password='fiapOn',  # Aspas adicionadas aqui
        database='dbfiapon'
    )
    
    # Conectar ao HDFS
    hdfs_client = InsecureClient('http://hadoop:9870', user='hadoop')

    try:
        with mysql_conn.cursor() as cursor:
            # Query específica para a tabela 2
            cursor.execute("SELECT * FROM tabela2")
            data = cursor.fetchall()

            # Transformação (ID, Descrição)
            transformed_data = [f"{item[0]}, {item[1]}" for item in data]

            # Salvar no HDFS com overwrite para evitar erro de arquivo já existente
            hdfs_path = '/user/hadoop/tabela2_output.txt'
            with hdfs_client.write(hdfs_path, encoding='utf-8', overwrite=True) as writer:
                for line in transformed_data:
                    writer.write(line + '\n')
    finally:
        # Garante que a conexão feche mesmo se houver erro no HDFS
        mysql_conn.close()

# Definição da DAG
with DAG(
    dag_id='dag2', 
    start_date=datetime(2023, 1, 1), 
    schedule_interval='@daily',
    catchup=False  # Evita que o Airflow tente rodar centenas de vezes o passado
) as dag:

    task1 = PythonOperator(
        task_id='transform_and_save_to_hadoop_t2', 
        python_callable=transform_and_save_to_hadoop
    )

    task1