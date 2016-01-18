from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config.from_object('config')
database = SQLAlchemy(app)
migrate = Migrate(app, database)
manager = Manager(app)
manager.add_command('database', MigrateCommand)




from web import views
from web import oauth
from web.domain import entities
