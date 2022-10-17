
import os
from datetime import datetime

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from auth import AuthError, requires_auth
from models import Auto, Buyer, setup_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    GET /autos
    Get all autos

    Example Request: curl 'http://localhost:5000/autos'

    Expected Result:
    {
        "autos": [
            {
            "buyers": [
                {
                "age": 54,
                "gender": "M",
                "id": 1,
                "auto_id": 2,
                "name": "Tom Hanks"
                },
                {
                "age": 45,
                "gender": "M",
                "id": 4,
                "auto_id": 2,
                "name": "Robert Downey, Jr."
                },
                {
                "age": 45,
                "gender": "F",
                "id": 5,
                "auto_id": 2,
                "name": "Julia Roberts"
                }
            ],
            "id": 2,
            "release_date": "Fri, 04 May 2012 00:00:00 GMT",
            "title": "Benz"
            },
            ...
        ],
        "success": true
    }
    '''
    @app.route('/autos', methods=['GET'])
    @requires_auth('view:autos')
    def retrieve_autos(payload):
        autos = Auto.query.all()
        autos = list(map(lambda auto: auto.format(), autos))
        return jsonify({
            "success": True,
            "autos": autos
        })

    '''
    GET /buyers
    Get all buyers

    Example Request: curl 'http://localhost:5000/buyers'

    Expected Result:
    {
        "buyers": [
            {
            "age": 45,
            "gender": "M",
            "id": 6,
            "auto_id": 1,
            "name": "Jack Hagen"
            },
            {
            "age": 54,
            "gender": "M",
            "id": 1,
            "auto_id": 2,
            "name": "John Smidth"
            },
            {
            "age": 44,
            "gender": "M",
            "id": 2,
            "auto_id": 3,
            "name": "Michael Brema"
            }
        ],
        "success": true
    }
    '''
    @app.route('/buyers', methods=['GET'])
    @requires_auth('view:buyers')
    def retrieve_buyers(payload):
        buyers = Buyer.query.all()
        buyers = list(map(lambda buyer: buyer.format(), buyers))
        return jsonify({
            "success": True,
            "buyers": buyers
        })

    '''
    POST /autos
    Creates a new auto.
    Requires the title and release date.

    Example Request: (Create)
    curl --location --request POST 'http://localhost:5000/autos' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "title": "Pek Yakında",
            "release_date": "2020-02-19"
        }'

    Example Response:
    {
        "success": true
    }
    '''
    @app.route('/autos', methods=['POST'])
    @requires_auth('post:autos')
    def create_auto(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title is None or release_date is None:
            abort(400, "Missing field for Auto")

        auto = Auto(title=title,
                      release_date=release_date)

        auto.insert()

        return jsonify({
            "success": True
        })

        '''
    POST /buyers
    Creates a new buyer.
    Requires the name, age and gender of the buyer.

    Example Request: (Create)
    curl --location --request POST 'http://localhost:5000/buyers' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "name": "Cem Yılmaz",
            "age": "45",
            "gender": "M"
        }'

    Example Response:
    {
        "success": true
    }
    '''
    @app.route('/buyers', methods=['POST'])
    @requires_auth('post:buyers')
    def create_buyer(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        auto_id = body.get('auto_id', None)

        if name is None or age is None or gender is None or auto_id is None:
            abort(400, "Missing field for Buyer")

        buyer = Buyer(name=name, age=age, gender=gender, auto_id=auto_id)

        buyer.insert()

        return jsonify({
            "success": True
        })

    '''
    DELETE /autos/<int:auto_id>
    Deletes the auto with given id

    Example Request: curl --request DELETE 'http://localhost:5000/autos/1'

    Example Response:
    {
        "deleted": 1,
        "success": true
    }
    '''
    @app.route('/autos/<int:auto_id>', methods=['DELETE'])
    @requires_auth('delete:autos')
    def delete_auto(payload, auto_id):
        auto = Auto.query.filter(Auto.id == auto_id).one_or_none()

        if auto is None:
            abort(404, "No auto with given id " + str(auto_id) + " is found")

        auto.delete()

        return jsonify({
            'success': True,
            'deleted': auto_id
        })

    '''
    DELETE /buyers/<int:buyer_id>
    Deletes the buyer with given id

    Example Request: curl --request DELETE 'http://localhost:5000/buyers/1'

    Example Response:
    {
        "deleted": 1,
        "success": true
    }
    '''
    @app.route('/buyers/<int:buyer_id>', methods=['DELETE'])
    @requires_auth('delete:buyers')
    def delete_buyer(payload, buyer_id):
        buyer = Buyer.query.filter(Buyer.id == buyer_id).one_or_none()

        if buyer is None:
            abort(404, "No buyer with given id " + str(buyer_id) + " is found")

        buyer.delete()

        return jsonify({
            'success': True,
            'deleted': buyer_id
        })

    '''
    PATCH /autos/<auto_id>
        Updates the auto where <auto_id> is the existing auto id
        Responds with a 404 error if <auto_id> is not found
        Update the corresponding fields for Auto with id <auto_id>

    Example Request:
    curl --location --request PATCH 'http://localhost:5000/autos/1' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "title": "Eyvah eyvah 2"
        }'

    Example Response:
    {
        "success": true,
        "updated": {
            "id": 1,
            "release_date": "Wed, 04 May 2016 00:00:00 GMT",
            "title": "Eyvah eyvah 2"
        }
    }
    '''
    @app.route('/autos/<int:auto_id>', methods=['PATCH'])
    @requires_auth('update:autos')
    def update_auto(payload, auto_id):

        updated_auto = Auto.query.get(auto_id)

        if not updated_auto:
            abort(
                404,
                'Auto with id: ' +
                str(auto_id) +
                ' could not be found.')

        body = request.get_json()

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title:
            updated_auto.title = title
        if release_date:
            updated_auto.release_date = release_date

        updated_auto.update()

        return jsonify({
            "success": True,
            "updated": updated_auto.format()
        })

    '''
    PATCH /buyers/<buyer_id>
        Updates the buyer where <buyer_id> is the existing buyer id
        Responds with a 404 error if <buyer_id> is not found
        Update the given fields for Buyer with id <buyer_id>

    Example Request:
    curl --location --request PATCH 'http://localhost:5000/buyers/1' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "name": "Tom Hanks"
        }'

    Example Response:
    {
        "success": true,
        "updated": {
            "age": 54,
            "gender": "M",
            "id": 1,
            "name": "Tom Hanks"
        }
    }
    '''
    @app.route('/buyers/<int:buyer_id>', methods=['PATCH'])
    @requires_auth('update:buyers')
    def update_buyer(payload, buyer_id):

        updated_buyer = Buyer.query.get(buyer_id)

        if not updated_buyer:
            abort(
                404,
                'Buyer with id: ' +
                str(buyer_id) +
                ' could not be found.')

        body = request.get_json()

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        auto_id = body.get('auto_id', None)

        if name:
            updated_buyer.name = name
        if age:
            updated_buyer.age = age
        if gender:
            updated_buyer.gender = gender
        if auto_id:
            updated_buyer.auto_id = auto_id

        try:
            updated_buyer.update()
        except BaseException:
            abort(
                400,
                "Bad formatted request due to nonexistent auto id" +
                str(auto_id))

        return jsonify({
            "success": True,
            "updated": updated_buyer.format()
        })

    def get_error_message(error, default_message):
        try:
            return error.description
        except BaseException:
            return default_message

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": get_error_message(error, "unprocessable"),
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": get_error_message(error, "resource not found")
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": get_error_message(error, "bad request")
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(auth_error):
        return jsonify({
            "success": False,
            "error": auth_error.status_code,
            "message": auth_error.error['description']
        }), auth_error.status_code

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)


