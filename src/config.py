import os

basedirectory = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = '!1234567890@#$%^&*()'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

SQL_DATABASE_NAME = 'database/webapp.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedirectory, SQL_DATABASE_NAME)
SQLALCHEMY_MIGRATE_REPO= os.path.join(basedirectory, 'db_repository')

OAUTH_CREDENTIALS = {'twitter': { 'id': 'prqSw94LQV4dUGL7EG8aXRNOP', 'secret': 'MzJ996mElLVMDa6oHGyswF9YqGkmjzfQ3BtSn6AOMFkpUoLtDs' }}

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['rdjnkr@gmail.com']