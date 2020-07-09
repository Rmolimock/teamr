#!/usr/bin/python3

if __name__ == "__main__":
    from datetime import datetime
    import pymongo

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["teamr"]

    mycol = mydb["__Base__"]

    mycol = mydb["users"]
    mycol.delete_many({})

    mydict = { "name": "John", "address": "Highway 37" }

    mydb.list_collections()

    class a:
        ids = 0
        def __init__(self):
            self.one = a.ids + 1
            a.ids += 1
            self.two = 'two'
            self.three = {'hello': 'there', 'hi': 3}
            self.test = b()
            self.test2 = [1, 2, 3]
            classname = '__' + str(self.__class__.__name__) + '__'
            mycol = mydb[classname]
            dict_repr = self.to_json()
            mycol.save(dict_repr)
        def remove_from_db(self):
            classname = '__' + str(self.__class__.__name__) + '__'
            mycol = mydb[classname]
            dict_repr = self.to_json()
            mycol.delete_one(dict_repr)
        def to_json(self) -> dict:
            """ Convert the object into a JSON dictionary """
            result = {}
            classname = '__' + str(self.__class__.__name__) + '__'
            result['__classname__'] = classname
            for key, value in self.__dict__.items():
                if type(value) is datetime:
                    result[key] = value.strftime(TIMESTAMP_FORMAT)
                else:
                    if hasattr(value, 'to_json'):
                        result[key] = value.to_json()
                    else:
                        result[key] = value
            return result
            
    
    class b:
        def __init__(self):
            self.g = 1234
        def to_json(self) -> dict:
            """ Convert the object into a JSON dictionary """
            result = {}
            classname = '__' + str(self.__class__.__name__) + '__'
            result['__classname__'] = classname
            for key, value in self.__dict__.items():
                if type(value) is datetime:
                    result[key] = value.strftime(TIMESTAMP_FORMAT)
                else:
                    if hasattr(value, 'to_json'):
                        result[key] = value.to_json()
                    else:
                        result[key] = value
            return result


    mycol.delete_many({})

    obj = a()
    obj2 = a()

    classname = '__' + str(obj.__class__.__name__) + '__'
    mycol = mydb[classname]
    for i in mycol.find():
        print(i)
    
    obj2.remove_from_db()
    print('after')
    res = {}
    res[classname] = []
    for i in mycol.find():
        res[classname].append(i)
        print(i)

    from flask import jsonify
    jsonify(res)


    
