import sys
import os

d = os.environ
os.environ.update({"IDEABAG": "production"})

from app import application