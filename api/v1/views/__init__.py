#!/usr/bin/env python3
"""
Store api routes in app_views blueprint
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="")

from api.v1.views.index import *