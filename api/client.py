import requests
from loguru import logger
BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE + "api/hw1000")
logger.info(response)
logger.info(response.json())