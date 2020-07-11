#!/usr/bin/env python3
import pymongo


client = pymongo.MongoClient("mongodb://localhost:33333/")
db = client.teamr
collection = db['User']