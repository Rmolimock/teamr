#!/usr/bin/env python3
import pymongo

client = pymongo.MongoClient("mongodb+srv://admin:LeErz4HubDEX4iHY@cluster0.e2stt.gcp.mongodb.net/teamr?retryWrites=true&w=majority")
db = client.teamr
users = db.User
users.insert_one({ "__classname__" : "User", "id" : "95ec1930-b399-4292-a07e-30394a993bee", "created_at" : "2020-07-13T21:26:46", "updated_at" : "2020-07-13T21:26:46", "username" : "a", "email" : "a@a.com", "password" : "a" })