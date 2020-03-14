
from flask import Flask
from app.models import Person, db

from sqlalchemy_utils import create_database, database_exists


def create_app():
	app = Flask(__name__)

	db.init_app(app)
	db_url = 'postgresql://testusr:password@127.0.0.1:5432/testdb'
	if not database_exists(db_url):
         create_database(db_url)

	return app

app = create_app()

@app.route('/', methods=['GET'])
def index():

	print(db.session.query(Person).all())

	return 'hi'
