from flask.ext.login import UserMixin, LoginManager
from hashlib import md5

from web import app
from web import database

lm = LoginManager(app)

class User(UserMixin, database.Model):
	__tablename__ = 'users'
	id = database.Column(database.Integer, primary_key=True)
	social_id = database.Column(database.String(64), nullable=True, unique=True)
	nickname = database.Column(database.String(64), nullable=False, index=True, unique=True)
	email = database.Column(database.String(120), nullable=False, index=True, unique=True)
	posts = database.relationship('Post', backref='author', lazy='dynamic')
	about_me = database.Column(database.String(140))
	last_seen = database.Column(database.DateTime)

	def __repr__(self):
		return '<User %r>' % (self.nickname)

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

	@lm.user_loader
	def load_user(id):
		return User.query.get(int(id))

	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)

	@staticmethod
	def make_unique_nickname(nickname):
		if User.query.filter_by(nickname=nickname).first() is None:
			return nickname
		version = User.query.count() + 1
		new_nickname = nickname + str(version)
		return new_nickname

	@property
	def serialize(self):
		"""User in a serialized format"""
		return {
		'social_id': self.social_id,
		'id': self.id,
		'username': self.username,
		'email': self.email
		}

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False
	

class Post(database.Model):
	__tablename__ = 'posts'
	id = database.Column(database.Integer, primary_key=True)
	body = database.Column(database.String(140))
	timestamp = database.Column(database.DateTime)
	user_id = database.Column(database.Integer, database.ForeignKey('users.id'))

	def __repr__(self):
		return '<Post %r>' % (self.body)