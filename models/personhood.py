#!/usr/bin/env python3
""" Personhood class """
from models import Base
from datetime import datetime

class Personhood(Base):
    """ Personhood class """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a Personhood object """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user')
        self.teams = []
        classname = str(self.__class__.__name__)
        self.profile_pic = f'https://thepointistochangeit.com/static/images/{classname}/{self.id}.png'