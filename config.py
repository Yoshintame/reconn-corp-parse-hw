import os, sys

from dotenv import load_dotenv

load_dotenv()

def check_and_set_env(env_name: str) -> str:
    if env_name in os.environ:
        var = os.getenv(env_name)
        return var
    else:
        raise EnvironmentError(f"Failed to because {env_name} is not set.")

CERTIFICATE_PASSWORD = check_and_set_env("CERTIFICATE_PASSWORD")
CORP_USERNAME = check_and_set_env("CORP_USERNAME")
CORP_PASSWORD = check_and_set_env("CORP_PASSWORD")