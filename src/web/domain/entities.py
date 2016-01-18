from flask.ext.login import UserMixin, LoginManager

from web import app
from web import database

lm = LoginManager(app)

class User(UserMixin, database.Model):
	__tablename__ = 'users'
	id = database.Column(database.Integer, primary_key=True)
	social_id = database.Column(database.String(64), nullable=False, unique=True)
	nickname = database.Column(database.String(64), nullable=False, index=True, unique=True)
	email = database.Column(database.String(120), nullable=False, index=True, unique=True)

	def __repr__(self):
		return '<User %r>' % (self.nickname)

	@lm.user_loader
	def load_user(id):
		return User.query.get(int(id))

	@property
	def serialize(self):
		"""User in a serialized format"""
		return {
		'social_id': self.social_id,
		'id': self.id,
		'username': self.username,
		'email': self.email
		}

class Post(database.Model):
	__tablename__ = 'posts'
	id = database.Column(database.Integer, primary_key=True)
	body = database.Column(database.String(140))
	timestamp = database.Column(database.DateTime)
	user_id = database.Column(database.Integer, database.ForeignKey('users.id'))

	def __repr__(self):
		return '<Post %r>' % (self.body)