
#datetime
from datetime import datetime

# The DAG object
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator


# Créer et utiliser des connections airflow pour se connecter à une base de donnée (postgresql)
dag_psql = DAG(
    dag_id = "postgresoperator_demo",
    default_args={'owner': 'sousou'},
    schedule_interval='@once',
    description='use case of psql operator in airflow',
    start_date=datetime(2022, 10, 13, 9),
	tags=['postgresql, db_airflow']
)
create_table_sql_query = """ 
CREATE TABLE employee (id INT NOT NULL, name VARCHAR(250) NOT NULL, dept VARCHAR(250) NOT NULL);
"""
insert_data_sql_query = """
insert into employee (id, name, dept) values(1, 'vamshi','bigdata'),(2, 'divya','bigdata'),(3, 'binny','projectmanager'),
(4, 'omair','projectmanager') ;"""
create_table_task = PostgresOperator(
    sql = create_table_sql_query,
    task_id = "create_table",
    postgres_conn_id = "postgres_default",
    dag = dag_psql
)
insert_data_task  = PostgresOperator(
    sql = insert_data_sql_query,
    task_id = "insert_data",
    postgres_conn_id = "postgres_default",
    dag = dag_psql
)
create_table_task >> insert_data_task