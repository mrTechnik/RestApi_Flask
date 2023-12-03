import unittest
from unittest.mock import patch
from app import app, db, Task, datetime
import json


class TestAppEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://localhost:5000'
        }

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_task(self):
        # Mock the request data
        task_data = {
            'name': 'Sample Task',
            'description': 'This is a sample task description.'
        }

        # Send a POST request to the endpoint
        response = self.app.post('/tasks', data=json.dumps(task_data), headers=self.headers)

        # Verify the response status code and JSON content
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['name'], 'Sample Task')
        self.assertEqual(response_data['description'], 'This is a sample task description.')

    def test_get_all_tasks(self):
        # create tasks for checking
        with app.app_context():
            db.create_all()
            task1 = Task(id=1, name='Task 1', description='Description 1', datetime_=datetime.now())
            task2 = Task(id=2, name='Task 2', description='Description 2', datetime_=datetime.now())
            db.session.add(task1)
            db.session.add(task2)
            db.session.commit()

        # test request for all tasks
        response = self.app.get('/tasks')
        data = json.loads(response.data)

        # check responce status 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check added tasks
        self.assertGreaterEqual(len(data), 2)

    def test_get_all_tasks_empty(self):
        # test responce for all tasks
        response = self.app.get('/tasks')
        data = json.loads(response.data)

        # create responce 500
        self.assertEqual(response.status_code, 500)
        # check error status
        self.assertIn('error', data)

    def test_get_task(self):
        with app.app_context():
            db.create_all()
            # create new task
            task = Task(id=1, name='Test Task', description='Test Description', datetime_=datetime.now())
            db.session.add(task)
            db.session.commit()

        # test request by ID
        response = self.app.get('/tasks/1')
        data = json.loads(response.data)

        # Проверяем, что статус ответа 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check response
        self.assertEqual(data['name'], 'Test Task')
        self.assertEqual(data['description'], 'Test Description')

    def test_update_task(self):
        with app.app_context():
            db.create_all()
            # Сcreate test task
            task = Task(id=1, name='Test Task', description='Test Description', datetime_=datetime.now())
            db.session.add(task)
            db.session.commit()

        # update task
        update_data = {'name': 'Updated Task', 'description': 'Updated Description'}
        response = self.app.put('/tasks/1', json=update_data)
        updated_data = json.loads(response.data)

        # Check response 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check that task was updated
        self.assertEqual(updated_data['name'], 'Updated Task')
        self.assertEqual(updated_data['description'], 'Updated Description')

    def test_delete_existing_task(self):
        with app.app_context():
            db.create_all()
            # create new task
            task = Task(id=1, name='Test Task', description='Test Description', datetime_=datetime.now())
            db.session.add(task)
            db.session.commit()

        # delete task
        response = self.app.delete('/tasks/1')
        data = json.loads(response.data)

        # Check answer status 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Проверяем, что задача была успешно удалена
        self.assertEqual(data['message'], 'Task deleted successfully')

    def test_delete_nonexistent_task(self):
        # delete noncreated tak
        response = self.app.delete('/tasks/1')
        data = json.loads(response.data)

        # check response code 500
        self.assertEqual(response.status_code, 500)
        # Check error code
        self.assertEqual(data['error'], 'We have an issue!!!')


if __name__ == '__main__':
    unittest.main()
