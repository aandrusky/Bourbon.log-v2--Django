import json
from rest_framework import status
from rest_framework.test import APITestCase
from bourbonLogServerAPI.models import FlavorSum, Flavor, Log


class FlavorSumTests(APITestCase):
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

        flavor = Flavor()
        flavor.flavor = "Spicy"
        flavor.save()

        log = Log()
        log.bourbon_name = "Eagle Rare"
        log.distiller = "Buffalo Trace"
        log.proof = "90"
        log.price = "35"
        log.age = "10"
        log.batch_num = "n/a"
        log.rating = "8/10"
        log.notes = "For $35 and 10 years old, you can't beat it!"
        log.owned = True
        log.logger_id = 1

        log.save()
    
    def test_create_flavorsum(self):
        """
        Ensure we can create a new game.
        """
        
        url = "/flavorsums"
        data = {
            "flavorId": 1,
            "flavorweight": 50,
            "logId": 1
               }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the flavorsum was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        
        self.assertEqual(json_response["flavor_weight"], 50)
        
    def test_get_all_flavors(self):
        """
        Ensure we can get a collection of products.
        """

        flavorsum = FlavorSum()
        flavorsum.flavor_id = 1
        flavorsum.flavor_weight = 40
        flavorsum.log_id = 1
        flavorsum.save()

        flavorsum = FlavorSum()
        flavorsum.flavor_id = 1
        flavorsum.flavor_weight = 50
        flavorsum.log_id = 1
        flavorsum.save()

        flavorsum = FlavorSum()
        flavorsum.flavor_id = 1
        flavorsum.flavor_weight = 60
        flavorsum.log_id = 1
        flavorsum.save()
        

        url = "/flavorsums"

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 3)