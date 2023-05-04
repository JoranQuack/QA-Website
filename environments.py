"""load env file variables"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path('.env'))

SALT = os.getenv('SALT')
SECRET_KEY = os.getenv('SECRET_KEY')
MAP_API_KEY = os.getenv('MAP_API_KEY')

assert SALT is not None
