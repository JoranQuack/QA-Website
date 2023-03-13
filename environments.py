"""load env file variables"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path('.env'))

SALT = os.getenv('SALT')
SECRET_KEY = os.getenv('SECRETKEY')
