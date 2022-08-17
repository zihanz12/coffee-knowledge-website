"""Setup at app startup"""
import os
import sqlalchemy
from yaml import load, Loader
from flask import Flask

app = Flask(__name__)

def init_connect_engine():
	if os.environ.get('GAE_ENV') != 'standard':
		variables = load(open("app.yaml"), Loader=Loader)
		env_variables = variables['env_variables']
		for var in env_variables:
			os.environ[var] = env_variables[var]

		pool = sqlalchemy.create_engine(
				sqlalchemy.engine.url.URL(
						drivername="mysql+pymysql",
						username=os.environ.get('MYSQL_USER'), #username
						password=os.environ.get('MYSQL_PASSWORD'), #user password
						database=os.environ.get('MYSQL_DB'), #database name
						host=os.environ.get('MYSQL_HOST'), #ip 
					)
			)
	else:
		pool = sqlalchemy.create_engine(
				sqlalchemy.engine.url.URL(
						drivername="mysql+pymysql",
						username=os.environ.get('MYSQL_USER'), #username
						password=os.environ.get('MYSQL_PASSWORD'), #user password
						database=os.environ.get('MYSQL_DB'), #database name
						query={"unix_socket": '/cloudsql/eighth-study-354817:us-central1:coffeestorysql'}
					)
			)
	return pool

db = init_connect_engine()

# To prevent from using a blueprint, we use a cyclic import
# This also means thaqt we need to place this import here
# pylint: disable=cyclic-import, wrong-import-position
from app import routes