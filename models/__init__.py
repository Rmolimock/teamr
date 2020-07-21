#!/usr/bin/env python3
from models.engine.mongodb import db

from models.base import *
from models.user import User
from models.nav_link import *

Base.load(db)
User.load(db)