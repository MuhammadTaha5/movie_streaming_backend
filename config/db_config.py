from pymongo import MongoClient
import urllib.parse

username = "tahasaeed339_db_user"
password = "taha4569"
cluster = "cluster0.lmpsiin.mongodb.net"

password_encoded = urllib.parse.quote_plus(password)
uri = f"mongodb+srv://{username}:{password_encoded}@{cluster}/?retryWrites=true&w=majority"

client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
db = client["movieDB"]

def get_db():
    return db

