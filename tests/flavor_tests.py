import json
from rest_framework import status
from rest_framework.test import APITestCase
from bourbonLogServerAPI.models import Flavor


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
        

        

    def test_get_all_flavors(self):
        """
        Ensure we can get a collection of products.
        """
        #create flavors to get
        flavor = Flavor()
        flavor.flavor = "Spicy"
        flavor.save()  
        flavor = Flavor()
        flavor.flavor = "Earthy"
        flavor.save()  
        flavor = Flavor()
        flavor.flavor = "Grain"
        flavor.save()  

        url = "/flavors"

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 3)


      



       