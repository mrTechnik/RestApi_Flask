from flask import Flask, request, jsonify
from sqlalchemy.sql.expression import func
from src.flask_sql_alchemy import *
import logging as lg
from flask_cors import CORS, cross_origin


# set logging
lg.basicConfig(filename='logs/app.log', level=lg.INFO)
# create Flask app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)
# logging app starting
lg.info(f"Application have started by: {str(datetime.now())}")
# set CORS resources
CORS(app, resources={
       r"*": {
           "origins": "https://localhost:5000",  # Разрешенный домен
           "methods": ["GET", "POST", "PUT", "DELETE"],  # Разрешенные типы запросов
           "allow_headers": ["Application/json"]  # Разрешенные заголовки
       }
   })


# init 404 catcher
@app.errorhandler(404)
def internal_server_error404(*args):
    return jsonify({'error': 'Bed request for a server!!!'}), 404


# init 500 catcher
@app.errorhandler(500)
def internal_server_error500(*args):
    return jsonify({'error': 'We have an issue!!!'}), 500


#start app
with app.app_context():
    # init SQLite db
    db.create_all()


    @app.route('/tasks', methods=['POST'])
    @cross_origin()
    def create_task():
        """
        API endpoint to create a new task.

        Request Body:
        - name: str
            The name of the task.
        - description: str
            The description of the task.

            Returns:
            - dict:
            A JSON response containing the created task details.
        """
        # Getting the task details from the request body
        task_data = request.get_json()
        if task_data:
            name = task_data.get('name')
            description = task_data.get('description')

            # Generating a unique identifier for the task
            task_id = db.session.query(func.max(Task.id)).scalar()
            # Check by None responce
            if task_id is None:
                task_id = 1
            else:
                task_id += 1
            # init new table entry
            task = Task(
                id=task_id,
                name=name,
                description=description,
                datetime_=datetime.now()
            )
            # add entry in the Task table
            db.session.add(task)
            db.session.commit()
            # logging a request
            lg.info(f"New task:{task.__class__}: "
                    f"id={task_id}: name={name}: description={description}: datetime_={str(datetime.now())}")
            # Returning the created task as a JSON response
            return jsonify(task.to_dict()), 201
        else:
            # Error message, task was now found
            lg.error(f"Task didn't created")
            # Returning a 404 error if the task is not found
            return jsonify({'error': 'Tasks didn\'t created'}), 404


    @app.route('/tasks', methods=['GET'])
    @cross_origin()
    def get_all_tasks():
        """
        API endpoint to get a list of all tasks.

        Returns:
        - dict:
            A JSON response containing the list of all tasks.
        """
        # Returning the list of tasks as a JSON response
        tasks = Task.query.all()
        if tasks:
            # logging a request
            lg.info(f"Get list of tasks: {tasks[0].__class__}")
            return jsonify(*(task.to_dict() for task in tasks)), 200
        else:
            # Error message, task was now found
            lg.error(f"Tasks not found")
            # Returning a 404 error if the task is not found
            return jsonify({'error': 'Tasks not found'}), 404


    @app.route('/tasks/<int:task_id>', methods=['GET'])
    @cross_origin()
    def get_task(task_id):
        """
        API endpoint to get a specific task by its ID.

        Parameters:
        - task_id: int
            The ID of the task to retrieve.

        Returns:
        - dict:
            A JSON response containing the details of the requested task.
        """

        # Searching for the task with the given ID
        task = Task.query.filter_by(id=task_id).first()
        if task is not None:
            # logging a request
            lg.info(f"Get list of tasks:{task.__class__}")
            # Returning the task as a JSON response
            return jsonify(task.to_dict()), 200
        else:
            # Error message, task was now found
            lg.error(f"Task not found: id={task_id}")
            # Returning a 404 error if the task is not found
            return jsonify({'error': 'Task not found'}), 404


    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    @cross_origin()
    def update_task(task_id):
        """
        API endpoint to update a specific task by its ID.

        Parameters:
        - task_id: int
            The ID of the task to update.

        Request Body:
        - name: str
            The updated name of the task.
        - description: str
            The updated description of the task.

        Returns:
        - dict:
            A JSON response containing the updated task details.
        """

        # Getting the updated task details from the request body
        task_data = request.get_json()
        name = task_data.get('name')
        description = task_data.get('description')
        # get task by id
        task = Task.query.filter_by(id=task_id).first()\

        if task is not None:
            # update task
            task.name = name
            task.description = description
            db.session.commit()
            # logging a request
            lg.info(f"Task was updated: {task.__class__}: "
                    f"id={task_id}: name={name}: description={description}: datetime_={str(datetime.now())}")
            # Returning the updated task as a JSON response
            return jsonify(task.to_dict()), 200
        else:
            # Error message, task was now found
            lg.error(f"Task not found: id={task_id}")
            # Returning a 404 error if the task is not found
            return jsonify({'error': 'Task not found'}), 404


    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    @cross_origin()
    def delete_task(task_id):
        """
        API endpoint to delete a specific task by its ID.

        Parameters:
        - task_id: int
            The ID of the task to delete.

        Returns:
        - dict:
            A JSON response indicating the success of the deletion.
        """
        task = Task.query.filter_by(id=task_id).first()
        # Searching for the task with the given ID
        if task:
            # delete task
            db.session.delete(task)
            db.session.commit()
            # logging a request
            lg.info(f"Delete Task: {task_id}")
            # Returning a success message as a JSON response
            return jsonify({'message': 'Task deleted successfully'}), 200
        else:
            # Error message, task was now found
            lg.error(f"Task not found: id={task_id}")
            # Returning a 404 error if the task is not found
            return jsonify({'error': 'Task not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
