#!/usr/bin/env python3
""" Team class """
from models import Base, Personhood


class Team(Personhood):
    """ Team class """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a Team object """
        super().__init__(*args, **kwargs)
        self.name = None
        self.description = None
        self.members = []
        self.moderators = []
        self.requests_to_join = []



a, b, c = Team(), Team(), Team()
a.name = 'Team A'
a.description = "This is a Team description for A."
b.name = 'Team B'
b.description = "This is a Team description for B."
c.name = 'Team C'
c.description = "This is a Team description for C."