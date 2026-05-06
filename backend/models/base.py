"""MongoDB client instance."""
from pymongo import MongoClient
from flask import current_app

_client = None


def get_db():
    global _client
    if _client is None:
        _client = MongoClient(current_app.config["MONGO_URI"])
    uri = current_app.config["MONGO_URI"]
    db_name = uri.split("/")[-1].split("?")[0] or "mess_voting"
    return _client[db_name]
