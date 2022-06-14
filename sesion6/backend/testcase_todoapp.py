import unittest

from server import create_app
from models import setup_db, Todo, TodoList
import json


class TestCaseTodoApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'test'
        self.database_path='postgresql://{}:{}@{}/{}'.format('postgres','123456', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_todo = {
            'description': 'new todo',
            'completed': False,
            'list_id': 1
        }

    def test_get_todos_success(self):
        self.client().post('/todos', json=self.new_todo)

        res = self.client().get('/todos')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_todos'])
        self.assertTrue(len(data['todos']))

    def test_get_todos_failed(self):
        res = self.client().get('/todos?page=10000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_update_todo_success(self):
        res0 = self.client().post('/todos', json=self.new_todo)
        data0 = json.loads(res0.data)
        updated_id = data0['created']

        res = self.client().patch('/todos/' + str(updated_id), json={'description': 'update description'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], str(updated_id))


    def test_update_todo_failed(self):
        res = self.client().patch('/todos/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_failed(self):
        res = self.client().delete('/todos/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_delete_success(self):
        res0 = self.client().post('/todos', json=self.new_todo)
        data0 = json.loads(res0.data)
        deleted_id = data0['created']

        res = self.client().delete('/todos/' + str(deleted_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], str(deleted_id))
        self.assertTrue(len(data['todos']))
        self.assertTrue(data['total_todos'])
        

    def test_create_todo_success(self):
        res = self.client().post('/todos', json=self.new_todo)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['todos']))
        self.assertTrue(data['total_todos'])


    def test_search_success_unprocessable(self):
        res = self.client().post('/todos', json={'search': 'new'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['todos'])
        self.assertTrue(data['total_todos'])


    def test_create_todo_failed_unprocessable(self):
        res = self.client().post('/todos', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')



    def tearDown(self):
        pass