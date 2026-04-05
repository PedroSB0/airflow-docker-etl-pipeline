## 🎓 Contexto Acadêmico

Este projeto foi desenvolvido durante a **Graduação em Data Science na FIAP**. 
O objetivo principal foi a criação de uma infraestrutura robusta para pipelines de dados, integrando tecnologias de Big Data e Orquestração.

* **Instituição:** FIAP (Faculdade de Informática e Administração Paulista)
* **Orientação:** Professor Thiago Rocco

🚀 Configurando Airflow com Docker e MySQL (FIAP Enterprise Challenge)
Este repositório contém a infraestrutura necessária para rodar o Apache Airflow integrado a um banco de dados MySQL e um cluster Hadoop, focado em projetos de Engenharia de Dados.

🛠️ O Desafio
Durante a inicialização do ambiente, enfrentamos dois problemas principais:

Dependências de Driver: A falta do driver pymysql no container do Airflow impedia a conexão com o banco MySQL.

Container "Zumbi": O container do Airflow completava as migrações do banco de dados e desligava logo em seguida, sem iniciar o Webserver.

💡 A Solução
1. Dockerfile (Customização)
Para que o Airflow consiga se comunicar com o MySQL, foi necessário criar um Dockerfile personalizado para instalar as bibliotecas de cliente do MySQL e o driver Python:

Dockerfile
FROM apache/airflow:2.5.0
USER root
RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc
USER airflow
RUN pip install pymysql cryptography
2. Docker Compose (O "Pulo do Gato")
O ajuste crucial foi a adição do comando command: standalone. Sem ele, o Airflow executa apenas as tarefas de ambiente e encerra o container. O modo standalone garante que o Webserver, o Scheduler e o Triggerer rodem continuamente.

YAML
  airflow:
    build: .
    container_name: airflow
    command: standalone
    environment:
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: mysql+pymysql://root:fiapOn@mysql/dbfiapon
      _AIRFLOW_DB_UPGRADE: "true"
      _AIRFLOW_WWW_USER_CREATE: "true"
      # ... (outras configurações)
    ports:
      - "8080:8080"
    depends_on:
      - mysql
📂 Estrutura do Projeto
./dags: Pasta local mapeada para o container onde ficam os scripts Python das DAGs.

mysql_data: Volume persistente para não perder os metadados do Airflow.

hadoop_data: Volume para persistência dos dados do HDFS.

🚀 Como Executar
Clone o repositório.

Certifique-se de que o Docker Desktop está rodando.

No terminal, execute:

Bash
docker-compose up -d --build
Acesse o Airflow em: http://localhost:8080 (admin/admin).

Acesse o Hadoop em: http://localhost:9870.

Demonstração do resultado final do Projeto
[FOTO](img/projetofinal.jpeg)
