import json
from rest_framework import status
from rest_framework.test import APITestCase
from bourbonLogServerAPI.models import FlavorSum


class FlavorTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
             "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created **Dont forget to add response code in register_user fucntion for other components
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        