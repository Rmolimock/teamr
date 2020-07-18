#!/usr/bin/env python3
import pymongo
import gridfs
client = pymongo.MongoClient("mongodb+srv://admin:LeErz4HubDEX4iHY@cluster0.e2stt.gcp.mongodb.net/teamr?retryWrites=true&w=majority")
db = client.teamr
gridfs = gridfs.GridFS(db, 'images')