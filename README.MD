## API Endpoints

Create New Task
```bash
$ curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"name": "Task 1", "description": "Task 1 description"}' ```
```json
{"id":1,"name": "Task 1", "description": "Task 1 description", "datetime_": current datetime}
```

Get <task_id> Task
```bash
$ curl -X GET http://localhost:5000/tasks/1'''
```json
{"id":1,"name": "Task 1", "description": "Task 1 description","datetime_": datetime}
```

Get all Tasks
```bash
$ curl -X GET http://localhost:5000/tasks/'''
```json
{"id":3,"name": "Task 1", "description": "Task 1 description","datetime_": datetime_1}
{"id":3,"name": "Task 2", "description": "Task 2 description","datetime_": datetime_2}
{"id":3,"name": "Task 3", "description": "Task 3 description","datetime_": datetime_3}
```
Update <task_id> Task
```bash
$ curl -X PUT http://localhost:5000/tasks/1 -H "Content-Type: application/json" -d '{"name": "New Task 1", "description": "New Task 1 description"}' ```
```json
{"id":1,"name": "New Task 1", "description": "New Task 1 description"}
```
Delete <task_id> Task
```bash
$ curl -X DELETE http://localhost:5000/tasks/1'''
```json
{'message': 'Task deleted successfully'}
```


## Usage

This project uses the [Flask](http://flask.pocoo.org/) framework to serve data through a simple web site platform locally. 

```
DokuScketch
	├── tests
	│    └── app_test.py
	├── src
	│   └── flask_sql_alchemy.py
	├── .gitignore
	├── requirements.txt
	├── README.MD   
	└── app.py
```

###Run server
The steps bellow will guide you through the project installation.  </br>
The following commands should be executed in your computer console at the project folder:

* Clone the project to your local repository workspace;

* Create a virtual environment for the imported application through the following command:
```
$ virtualenv <Virtual Environment name>
```
* Activate your virtual environment with the command:
```
$ <Virtual Environment name>\Scripts\activate
```
 * With the virtual environment properly activated, install the plugins available at the **requirements.txt** file through the command:
```
$ pip install -r requirements.txt
```
This process should enable your application to be deployed in a local server for test purpose.

----------
Deployment
-------------
```
$ python run.py
```
