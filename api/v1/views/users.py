#!/usr/bin/python3
"""Handle user rest apis"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from models import storage
