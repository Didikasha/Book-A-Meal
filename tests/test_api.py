'''Test Book-A-MEAL endpoints'''

import unittest
import os
import json
import random
from Book-A-meal-api import app


class BookAMealTestcase(unittest.TestCase):
   '''class to tests app.py'''


def setUp(self):
        # binds the app to the current context
        with app.app.app_context():
            self.client = app.app.test_client


def test_api_can_get_all_meals(self):
      '''test that API can get a meal (GET request)'''
      response = self.client().get('/api/v1/meals')
      self.assertEqual(response.status_code, 200)


def test_api_can_add_a_meal(self):
    '''test that API can add a meal (POST request)'''
    response = self.client().get('/ap1/v1/meals' data=json.dumps({"meal_id": 1,
                                                             "name": "Pork and Fries",
                                                             , }),
                                            content_type='application/json')
    self.assertEqual(response.status_code, 200)


def test_meal_can_be_edited(self):
        '''test that api can modify meal'''
        self.client().post('/api/v1/meals', data=json.dumps({"meal_id": 21,
                                                             "name": "Pork and Fries",
                                                             }),
                                            content_type='application/json')
        res = self.client().put('/api/v1/meals/21',
                                data=json.dumps({"name": "Pork and Fries",
                                                 }),
                                content_type='application/json')
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/api/v1/meals/21')
        self.assertIn("John Greene", str(results.data))


def test_api_can_get_meal_by_id(self):
    '''test that api can retrieve meal by id (GET request)'''
    res = self.client().post('/ap1/v1/meals'data=json.dumps({"meal_id": 1,
                                                             "name": "Pork and Fries",
                                                             , }),
                                            content_type='application/json')
    self.assertEqual(result.status_code, 200)


def test_delete_meal(self):
        '''test that api can delete meal (POST request)'''
        res = self.client().post('/api/v1/meals', content_type='application/json',
                                 data=json.dumps({"meal_id": 16,
                                                  "name": "Pork and Fries",
                                                  }))
        self.assertEqual(res.status_code, 200)
        res = self.client().delete('/api/v1/meals/16')
        self.assertEqual(res.status_code, 200)

        # test to check whether deleted meal exists
        result = self.client().get('/api/v1/meals/16')
        self.assertIn("meal not found", result.data)

    def test_user_actions(self):
        '''method to test register, login, order meal and logout endpoints'''
        # test register
        result = self.client().post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps({"username":"Didi", "name":"Didi Kashemwa",
                                                     "email":"didi@dmail.com", "password":"cats",
                                                     "confirm_password":"cats"}))
        self.assertEqual(result.status_code, 201)
        self.assertIn("user registered successfully", result.data)

        # test login
        result2 = self.client().post('/api/v1/auth/login', content_type='application/json',
                                     data=json.dumps({"username":"Didi", "password":"cats"}))
        my_data = ast.literal_eval(result2.data)
        a_token = my_data["token"]
        self.assertEqual(result2.status_code, 200)
        self.assertEqual("Login successful", my_data["message"])

        # test order meal
        self.client().post('/api/v1/meals',
                                data=json.dumps({"name": "Spicy Pilau and beef",
                                                  , "meal_id":32}),
                                content_type='application/json')
        result3 = self.client().post('/api/v1/users/meals/32',
                                     headers=dict(Authorization="Bearer "+ a_token))
        self.assertEqual(result3.status_code, 200)
        self.assertIn("meal successfully checked out", result3.data)

        # test logout 
        result4 = self.client().post('/api/v1/auth/logout',
                                     headers=dict(Authorization="Bearer " + a_token))
        self.assertEqual(result4.status_code, 200)
        self.assertIn('Successfully logged out', result4.data)


    def test_reset_password(self):
        '''test reset password method = "POST"'''
        result = self.client().post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps({"username": "Dee", "name": "avocado",
                                                     "email": "Dee@hot.com", "password": "1234",
                                                     "confirm_password": "1234"}))
        self.assertEqual(result.status_code, 201)

        result2 = self.client().post('/api/v1/auth/reset-password', content_type="application/json",
                                    data=json.dumps({"username":"Dee"}))
        self.assertEqual(result2.status_code, 200)

if __name__ == "__main__":
    unittest.main()


    
