import os, sys

from dotenv import load_dotenv

load_dotenv()

def check_and_set_env(env_name: str) -> str:
    if env_name in os.environ:
        var = os.getenv(env_name)
        return var
    else:
        raise EnvironmentError(f"Failed to because {env_name} is not set.")

CORP_USERNAME = check_and_set_env("CORP_USERNAME")
CORP_PASSWORD = check_and_set_env("CORP_PASSWORD")

TELEGRAM_BOT_API_TOKEN = check_and_set_env("TELEGRAM_BOT_API_TOKEN")
TELEGRAM_API_ID = int(check_and_set_env("TELEGRAM_API_ID"))
TELEGRAM_API_HASH = check_and_set_env("TELEGRAM_API_HASH")


# Parser
# CRT_PATH =
# KEY_PATH =
# PEM_PATH =