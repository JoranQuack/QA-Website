from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=Path('.env'))

SALT = os.getenv('SALT')
SECRET_KEY = os.getenv('SECRETKEY')