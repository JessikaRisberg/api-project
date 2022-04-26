import os
from abc import ABC

import dotenv
from pymongo import MongoClient

dotenv.load_dotenv()

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_DATABASE = os.environ.get('DB_DATABASE')

client = MongoClient(f'mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}')
db = client[DB_DATABASE]
