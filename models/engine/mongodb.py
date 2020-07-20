#!/usr/bin/env python3
import pymongo
import gridfs


class DB():
    """ Database class """
    def __init__(self):
        """ init instance of DB """
        self.client = pymongo.MongoClient("mongodb+srv://admin:LeErz4HubDEX4iHY@cluster0.e2stt.gcp.mongodb.net/teamr?retryWrites=true&w=majority")
        self._db = self.client.teamr
    def hash_password(self, password):
        """
        ----------------------------
        Hash a given password.
        ----------------------------
        -> Return: Hashed version of password.
        """
        import bcrypt
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    def is_strong_password(self, pwd):
        """
        ----------------------------
        Check if:
            1. password is > 8 chars,
            2. password contains at least one special character,
            3. password contains at least one number.
        ----------------------------
        -> Return: True or appropriate error message.
        """
        if len(pwd) < 8:
            return 'Password must be at least 8 characters.'
        special_chars = '~`!@#$%^&*()_+={[}]|"\';:?/>.<,'
        numbers = "1234567890"
        spc = False
        nbs = False
        for c in pwd:
            if c in special_chars:
                spc = True
        for c in pwd:
            if c in numbers:
                nbs = True
        if not spc or not nbs:
            return 'Password must contain a special character and a number.'
        return True
    def register(self, username, email, pwd):
        """
        ----------------------------
        Register a new user into the database and memory.
        ----------------------------
        -> Return: Newly created User object or error message.
        """
        from models.user import User
        is_strong = self.is_strong_password(pwd)
        if type(is_strong) == str:
            return is_strong
        user_dict = {'email': email}
        if len(User.search(user_dict)) > 0:
            return 'User already exists.'
        print(User.search(user_dict))
        user = User(**user_dict)
        user.username = username
        pwd = self.hash_password(pwd)
        user.password = pwd
        self.save_obj(user)
        return user
    def save_obj(self, obj):
        """
        ----------------------------
        Save an object to the database and memory.
        ----------------------------
        -> Return: None.
        """
        classname = str(obj.__class__.__name__)
        mycol = self._db[classname]
        dict_repr = obj.to_json()
        mycol.save(dict_repr)
    def delete_obj(self, obj):
        """
        ----------------------------
        Delete an object from the db and memory.
        ----------------------------
        -> Return: None.
        """
        classname = str(obj.__class__.__name__)
        mycol = self._db[classname]
        dict_repr = obj.to_json()
        mycol.delete_one(dict_repr)
    def load_class(self, cls):
        """
        ----------------------------
        Load all instances of a class from the db into memory.
        ----------------------------
        -> Return: None.
        """
        mycol = self._db[cls.__name__]
        for each in mycol.find():
            print('*')
            obj = cls(**each)
    def save_session(self, auth):
        """
        ----------------------------
        Save a session into the db and memory.
        ----------------------------
        -> Return: None.
        """
        from api.v1.views.auth.auth import Auth
        mycol = self._db.sessions
        user_id_and_session_exp = Auth.session_ids[auth.id]
        session = {auth.id: user_id_and_session_exp}
        mycol.save(session)


db = DB()
gridfs = gridfs.GridFS(db._db, 'images')