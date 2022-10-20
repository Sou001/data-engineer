

#datetime
from datetime import timedelta, datetime

# The DAG object
from airflow import DAG

# Operators
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

## optionnel 
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.models import Variable


## write files with date of execution
## Créer un fichier avec : world & la date d'exec
def write_dtexecution(execution_date):
	date = execution_date.strftime("%m_%d_%Y - %H:%M:%S")
	f = open("/home/simplon/Documents/airflow/"+date+".txt","w")
	f.write("world " + date)
	f.close()

## optionnel : On utilise les variables de airflow & return the id defined for test
def return_id():
	return Variable.get("iddefined")

## Contient la tâche obligatoire & optionnelle : 
	# Générer un fichier dont le nom contient la date d'exécution du workflow
	# optionnelle en passant l'id d'une tâche à une autre
def execute_diffrent_tasks(**context):
	write_dtexecution(context["execution_date"])
	return return_id()

# Instantiate a DAG object
## hourly launch with start today at 9AM
with DAG('hourly_launch',
		default_args={'owner': 'sousou'},
		description='Hello World DAG',
		schedule_interval=timedelta(hours=1),
		start_date=datetime(2022,10,13,9),
		catchup=False,
		tags=['example, hourly_launch']) as dag:

	# Obligatoire task 1 :
		# Ajouter un dummy operator au DAG et le nommer start
	start = DummyOperator(task_id='start', dag=dag)

	# Obligatoire task 2 :
		# Ajouter une tâche utilisant le bash operator la nommer "list" et 
		# lui faire exécuter la commande "ls"
	list_bash_operator = BashOperator(task_id="list", 
									  dag=dag,
									  bash_command='ls /home/simplon/Documents')

	# optionnel - détecter drop file
	sensor_task = FileSensor( task_id= "file_sensor_task", 
							  poke_interval= 1, 
							  filepath= '/home/simplon/Documents/airflow/tst_sensor',
							  dag=dag)
	
	# Obligatoire task 3 :
		# Ajouter une tâche utilisant le python opérateur la nommer "hello" et
		# lui faire écrire un fichier contenant le mot "world" et contenant la date 
		# d'execution du workflow
	hello = PythonOperator(task_id='hello', 
						   python_callable=execute_diffrent_tasks,
						   provide_context=True,
						   dag=dag,
						   do_xcom_push=True)

	## optionnel : print la donnée transmise par la tâche hello
	printvalue = BashOperator(task_id="printvalue",
						   	  dag=dag,
						   	  bash_command='echo {{ task_instance.xcom_pull(task_ids="hello") }}'
							 )
	# Obligatoire task 4 :
		# Tache sleep en bash pour 10s
	sleep10 = BashOperator(task_id="sleep10",
						   dag=dag,
						   bash_command='sleep 10')
	
		# Tache sleep en bash pour 15s
	sleep15 = BashOperator(task_id="sleep15",
						   dag=dag,
						   bash_command='sleep 15')
	# Obligatoire task 5 :
	join = DummyOperator(task_id='join',
						 dag=dag)

# cheminement de l'exécution des opérateurs avec le bitshift >>
start >> sensor_task >> list_bash_operator >> hello >> printvalue >> [sleep10,sleep15] >> join