from pymongo import MongoClient

client = MongoClient()
real_db = client.cards_real
test_db = client.cards_test
