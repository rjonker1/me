from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from web import app
from web import database, migrate, manager

manager.add_command('database', MigrateCommand)
manager.run()
#manager.add_command(app.config['SQL_DATABASE_NAME'], MigrateCommand)



#from migrate.versioning import api
#from config import SQLALCHEMY_DATABASE_URI
#from config import SQLALCHEMY_MIGRATE_REPO
#from app import database
#import os.path

#database.create_all()
#if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
#	api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
#	api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
#else:
#	api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))