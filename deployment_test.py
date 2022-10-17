import json
import os
import unittest

import requests

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.api = "https://casting-agency-fsnd-kml.herokuapp.com"

        self.auto = {
            "title": "Pek Yakında",
            "release_date": "19-02-2020"
        }

        self.buyer = {
            "name": "Cem Yılmaz",
            "age": 45,
            "gender": 'M',
            "auto_id": 2
        }

        # Set up authentication tokens info
        with open('auth_config.json', 'r') as f:
            self.auth = json.loads(f.read())

        assistant_jwt = self.auth["roles"]["Sell Assistant"]["jwt_token"]
        director_jwt = self.auth["roles"]["Sell Manager"]["jwt_token"]
        producer_jwt = self.auth["roles"]["Executive Producer"]["jwt_token"]
        self.auth_headers = {
            "Sell Assistant": f'Bearer {assistant_jwt}',
            "Sell Manager": f'Bearer {director_jwt}',
            "Executive Producer": f'Bearer {producer_jwt}'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_autos(self):
        header_obj = {
            "Authorization": self.auth_headers["Sell Assistant"]
        }
        res = requests.get(self.api + '/autos', headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["autos"]), type([]))

    def test_get_buyers(self):
        header_obj = {
            "Authorization": self.auth_headers["Sell Assistant"]
        }
        res = requests.get(self.api + '/buyers', headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["buyers"]), type([]))

    def test_get_buyers_by_director(self):
        header_obj = {
            "Authorization": self.auth_headers["Sell Manager"]
        }
        res = requests.get(self.api + '/buyers', headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["buyers"]), type([]))

    def test_get_buyer_fail_401(self):
        res = requests.get(self.api + '/buyers')
        data = res.json()

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(type(data["message"]), type(""))

    def test_create_autos_fail_400(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        auto_fail = {"title": "auto"}
        res = requests.post(
            self.api + f'/autos',
            json=auto_fail,
            headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Missing field for auto")

    def test_create_autos_fail_403(self):
        header_obj = {
            "Authorization": self.auth_headers["Sell Manager"]
        }
        auto_fail = {"title": "auto"}
        res = requests.post(
            self.api + f'/autos',
            json=auto_fail,
            headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_create_buyers_fail_400(self):
        header_obj = {
            "Authorization": self.auth_headers["Sell Manager"]
        }
        buyer_fail = {"name": "buyer"}
        res = requests.post(
            self.api + f'/buyers',
            json=buyer_fail,
            headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Missing field for buyer")

    def test_create_buyers_fail_403(self):
        header_obj = {
            "Authorization": self.auth_headers["Sell Assistant"]
        }
        buyer_fail = {"name": "buyer"}
        res = requests.post(
            self.api + f'/buyers',
            json=buyer_fail,
            headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()



