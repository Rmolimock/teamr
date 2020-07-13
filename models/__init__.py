#!/usr/bin/env python3
from models.engine.mongodb import db

from models.base import Base
from models.user import User

Base.load(db)
User.load(db)