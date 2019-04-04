from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os
import json

db = create_engine("postgresql+psycopg2://zemoso:Miku1506@54.236.34.225:5432/zemoso")
db.echo = True
base = declarative_base()   
