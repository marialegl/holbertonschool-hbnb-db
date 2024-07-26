#!/usr/bin/python3
import json
import unittest

from api.api_controller import app, data_manager


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Crear una nueva instancia de data_manager para cada prueba
        self.data_manager = data_manager
        self.data_manager.storage = {'Users': {}}

    def tearDown(self):
        # Asegúrate de limpiar el estado después de cada prueba
        self.data_manager.storage = {'Users': {}}

    def test_create_user(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword'
        }
        response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['email'], 'john.doe@example.com')

    def test_create_user_invalid_email(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email',
            'password': 'securepassword'
        }
        response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        try:
            data = json.loads(response.data)
            self.assertIn('error', data)
        except json.JSONDecodeError:
            self.fail("La respuesta no es un JSON válido.")

    def test_create_user_existing_email(self):
        user_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'password': 'securepassword'
        }
        self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 409)
        try:
            data = json.loads(response.data)
            self.assertIn('error', data)
        except json.JSONDecodeError:
            self.fail("La respuesta no es un JSON válido.")

    def test_get_users(self):
        user_data_1 = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword'
        }
        user_data_2 = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'password': 'securepassword'
        }
        self.app.post('/users', data=json.dumps(user_data_1), content_type='application/json')
        self.app.post('/users', data=json.dumps(user_data_2), content_type='application/json')
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        try:
            data = json.loads(response.data)
            self.assertEqual(len(data), 2)
        except json.JSONDecodeError:
            self.fail("La respuesta no es un JSON válido.")

    def test_get_user(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword'
        }
        create_response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        user_id = json.loads(create_response.data)['id']
        response = self.app.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        try:
            data = json.loads(response.data)
            self.assertEqual(data['id'], user_id)
        except json.JSONDecodeError:
            self.fail("La respuesta no es un JSON válido.")

    def test_update_user(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword'
        }
        create_response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        user_id = json.loads(create_response.data)['id']
        update_data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.smith@example.com',
            'password': 'newsecurepassword'
        }
        response = self.app.put(f'/users/{user_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        try:
            data = json.loads(response.data)
            self.assertEqual(data['last_name'], 'Smith')
            self.assertEqual(data['email'], 'john.smith@example.com')
        except json.JSONDecodeError:
            self.fail("La respuesta no es un JSON válido.")

    def test_delete_user(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword'
        }
        create_response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        user_id = json.loads(create_response.data)['id']
        response = self.app.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 204)
        get_response = self.app.get(f'/users/{user_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_invalid_uuid(self):
        invalid_user_id = 'invalid-uuid'
        response = self.app.get(f'/users/{invalid_user_id}')
        self.assertEqual(response.status_code, 400)
        try:
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Invalid user ID')
        except json.JSONDecodeError:
            self.fail("La respuesta no es un JSON válido.")


if __name__ == '__main__':
    unittest.main()
