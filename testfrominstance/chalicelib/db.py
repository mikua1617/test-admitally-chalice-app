from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from .aws_secrets_helper import get_secret
import json

db = create_engine(json.loads(get_secret())["DB_URI"])
db.echo = True

base = declarative_base()
