from flask import Flask
from flask_restful import Api, Resource
import requests

from parser import parse_hw_page, corp_authentication, headers

app = Flask(__name__)
api = Api(app)

class PublicApi(Resource):
    def post(self, hw_number):
        hw_data = parse_hw_page(corp_session, headers, hw_number)

        return hw_data

    # def post(self):
    #     return {""}

api.add_resource(PublicApi, "/api/hw<int:hw_number>")


if __name__ == "__main__":
    corp_session = requests.Session()
    corp_authentication(corp_session, headers)

    app.run(debug=True)

