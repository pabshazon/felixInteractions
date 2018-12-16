#@todo: the app and the flask db manager use different ways of importing a package or .package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from .config import app_config


app = Flask(__name__)
app.config.from_object(app_config['development'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)


from .routes import *

if __name__ == '__main__':
    app.run(port=3000)



