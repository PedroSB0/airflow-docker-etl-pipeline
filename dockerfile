FROM apache/airflow:2.5.0-python3.8

# Voltamos para o usuário padrão do airflow para evitar o bloqueio de segurança
USER airflow

# Instalamos as bibliotecas na pasta de usuário (que o airflow tem permissão)
RUN pip install --no-cache-dir --user pymysql hdfs