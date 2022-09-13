import requests
from loguru import logger
BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "helloworld")
logger.info(response.json())