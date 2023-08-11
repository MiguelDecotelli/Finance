import json

with open('credentials.json') as json_file:
    config = json.load(json_file)

USER = config.get("USER")
PASSWORD = config.get("PASSWORD")
HOST = config.get("HOST")
DATABASE = config.get("DATABASE")
PORT =  21689
SECRET_KEY =  config.get("SECRET_KEY")