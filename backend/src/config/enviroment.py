import os

from dotenv import load_dotenv


class EnvNotFound(Exception):
    pass

load_dotenv()

def get_env(env: str):
    ENV = os.getenv(env)
    if not ENV:
        raise EnvNotFound(env)
    return ENV