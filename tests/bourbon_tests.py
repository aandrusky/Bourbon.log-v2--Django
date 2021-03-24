import json
from rest_framework import status
from rest_framework.test import APITestCase
from bourbonLogServerAPI.models import Log


class BourbonTests(APITestCase):
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
        

    def test_create_log(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE LOG PROPERTIES
        url = "/logs"
        data = {
            "bourbon_name": "Eagle Rare",
            "distiller": "Buffalo Trace",
            "proof": "90",
            "price": "35",
            "age": "10",
            "batch_num": "n/a",
            "rating": "8/10",
            "notes": "For $35 and 10 years old, you can't beat it!",
            "owned": True
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["bourbon_name"], "Eagle Rare")
        self.assertEqual(json_response["distiller"], "Buffalo Trace")
        self.assertEqual(json_response["proof"], "90")
        self.assertEqual(json_response["price"], "35")
        self.assertEqual(json_response["age"], "10")
        self.assertEqual(json_response["batch_num"], "n/a")
        self.assertEqual(json_response["rating"], "8/10")
        self.assertEqual(json_response["notes"], "For $35 and 10 years old, you can't beat it!")
        self.assertEqual(json_response["owned"], True)

    def test_get_log(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a log
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

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/logs/{log.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the log was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["bourbon_name"], "Eagle Rare")
        self.assertEqual(json_response["distiller"], "Buffalo Trace")
        self.assertEqual(json_response["proof"], "90")
        self.assertEqual(json_response["price"], "35")
        self.assertEqual(json_response["age"], "10")
        self.assertEqual(json_response["batch_num"], "n/a")
        self.assertEqual(json_response["rating"], "8/10")
        self.assertEqual(json_response["notes"], "For $35 and 10 years old, you can't beat it!")
        self.assertEqual(json_response["owned"], True)

    def test_update_log(self):
        """
        Ensure we can change an existing log.
        """
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

        # DEFINE NEW PROPERTIES FOR LOG
        data = {
            "bourbon_name": "Elijah Craig",
            "distiller": "Heaven Hill",
            "proof": "95",
            "price": "45",
            "age": "11",
            "batch_num": "B20",
            "rating": "9/10",
            "notes": "Delicious!",
            "owned": False
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/logs/{log.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/logs/{log.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["bourbon_name"], "Elijah Craig")
        self.assertEqual(json_response["distiller"], "Heaven Hill")
        self.assertEqual(json_response["proof"], "95")
        self.assertEqual(json_response["price"], "45")
        self.assertEqual(json_response["age"], "11")
        self.assertEqual(json_response["batch_num"], "B20")
        self.assertEqual(json_response["rating"], "9/10")
        self.assertEqual(json_response["notes"], "Delicious!")
        self.assertEqual(json_response["owned"], False)

    def test_delete_log(self):
        """
        Ensure we can delete an existing log.
        """
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

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/logs/{log.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/logs/{log.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)