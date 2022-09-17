from loguru import logger
from flask import Flask
from flask_restful import Api, Resource
import requests

from parser.parser import parse_hw_page, corp_authentication, headers
from telegram_bot.utils import create_hw_data_message
from telegram_bot.bot_handlers import send_message_as_bot

app = Flask(__name__)
api = Api(app)

class PublicApi(Resource):
    def post(self, hw_number: str):
        hw_data = parse_hw_page(corp_session, headers, hw_number)
        logger.info(hw_data)
        message = create_hw_data_message(hw_data)

        logger.info(message)
        # send_message_as_bot(user="yoshintame",message=message)
        return hw_data


api.add_resource(PublicApi, "/api/hw<int:hw_number>")


if __name__ == "__main__":
    corp_session = requests.Session()
    corp_authentication(corp_session, headers)

    app.run(debug=True)

