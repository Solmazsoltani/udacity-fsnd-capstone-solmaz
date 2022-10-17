import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import Auto, Buyer, setup_db


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.auto = {
            "title": "Pek Yakında",
            "release_date": "2020-11-02"
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

        assistant_jwt = self.auth["roles"]["Casting Assistant"]["jwt_token"]
        director_jwt = self.auth["roles"]["Casting Director"]["jwt_token"]
        producer_jwt = self.auth["roles"]["Executive Producer"]["jwt_token"]
        self.auth_headers = {
            "Casting Assistant": f'Bearer {assistant_jwt}',
            "Casting Director": f'Bearer {director_jwt}',
            "Executive Producer": f'Bearer {producer_jwt}'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_autos(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().get('/autos', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["autos"]), type([]))

    def test_get_buyers(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().get('/buyers', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["buyers"]), type([]))

    def test_get_buyers_by_director(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        res = self.client().get('/buyers', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["buyers"]), type([]))

    def test_get_buyer_fail_401(self):
        res = self.client().get('/buyers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(type(data["message"]), type(""))

    def test_create_autos(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().post(f'/autos',
                                 json=self.auto, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_autos_fail_400(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        auto_fail = {"title": "Auto"}
        res = self.client().post(f'/autos',
                                 json=auto_fail, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Missing field for Auto")

    def test_create_autos_fail_403(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        auto_fail = {"title": "Auto"}
        res = self.client().post(f'/autos',
                                 json=auto_fail, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_create_buyers(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        res = self.client().post(f'/buyers',
                                 json=self.buyer, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_buyers_fail_400(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        buyer_fail = {"name": "Buyer"}
        res = self.client().post(f'/buyers',
                                 json=buyer_fail, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Missing field for Buyer")

    def test_create_buyers_fail_403(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        buyer_fail = {"name": "Buyer"}
        res = self.client().post(f'/buyers',
                                 json=buyer_fail, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_auto(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        delete_id_auto = 1
        res = self.client().delete(
            f'/autos/{delete_id_auto}',
            headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], delete_id_auto)

        res = self.client().get('/autos', headers=header_obj)
        m_data = json.loads(res.data)

        found_deleted = False

        for m in m_data["autos"]:
            if m["id"] == delete_id_auto:
                found_deleted = True
                break

        self.assertFalse(found_deleted)

    def test_delete_auto_fail_404(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        m_id = 100
        res = self.client().delete(f'/autos/{m_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_auto_fail_403(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        m_id = 3
        res = self.client().delete(f'/autos/{m_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_buyer(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        delete_id_buyer = 1
        res = self.client().delete(
            f'/buyers/{delete_id_buyer}',
            headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], delete_id_buyer)

        res = self.client().get('/buyers', headers=header_obj)
        a_data = json.loads(res.data)

        found_deleted = False

        for a in a_data["buyers"]:
            if a["id"] == delete_id_buyer:
                found_deleted = True
                break

        self.assertFalse(found_deleted)

    def test_delete_buyer_fail_404(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        a_id = -100
        res = self.client().delete(f'/buyers/{a_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_buyer_fail_403(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        a_id = 100
        res = self.client().delete(f'/buyers/{a_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_update_auto(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        update_id_auto = 2
        new_title = "Eyvah eyvah 2"
        res = self.client().patch(
            f'/autos/{update_id_auto}',
            json={
                'title': new_title},
            headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated']['id'], update_id_auto)
        self.assertEqual(data['updated']['title'], new_title)

    def test_update_auto(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        update_id_auto = 2
        new_title = "Eyvah eyvah 2"
        res = self.client().patch(
            f'/autos/{update_id_auto}',
            json={
                'title': new_title},
            headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated']['id'], update_id_auto)
        self.assertEqual(data['updated']['title'], new_title)

    def test_update_auto_fail_404(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        update_id_auto = -100
        res = self.client().patch(
            f'/autos/{update_id_auto}',
            headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_update_buyer(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        update_id_buyer = 2
        new_name = "Tom Hanks"
        new_age = 54
        res = self.client().patch(
            f'/buyers/{update_id_buyer}',
            json={
                'name': new_name,
                'age': new_age},
            headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated']['id'], update_id_buyer)
        self.assertEqual(data['updated']['name'], new_name)
        self.assertEqual(data['updated']['age'], new_age)

    def test_update_buyer_fail_404(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        update_id_buyer = 100
        res = self.client().patch(
            f'/buyers/{update_id_buyer}',
            headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_update_buyer_fail_403(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        update_id_buyer = 100
        res = self.client().patch(
            f'/buyers/{update_id_buyer}',
            headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


