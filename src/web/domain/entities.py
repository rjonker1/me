from flask.ext.login import UserMixin, LoginManager
from hashlib import md5

from web import app
from web import database

lm = LoginManager(app)

followers = database.Table(
	'followers', 
	database.Column('follower_id', database.Integer, database.ForeignKey('user.id')),
	database.Column('followed_id', database.Integer, database.ForeignKey('user.id'))
	)


class User(UserMixin, database.Model):
	__tablename__ = 'user'
	id = database.Column(database.Integer, primary_key=True)
	social_id = database.Column(database.String(64), nullable=True, unique=True)
	nickname = database.Column(database.String(64), nullable=False, index=True, unique=True)
	email = database.Column(database.String(120), nullable=False, index=True, unique=True)
	posts = database.relationship('Post', backref='author', lazy='dynamic')
	about_me = database.Column(database.String(140))
	last_seen = database.Column(database.DateTime)
	followed = database.relationship('User',
		secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref=database.backref('followers', lazy='dynamic'),
		lazy='dynamic')

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

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % \
		(md5(self.email.encode('utf-8')).hexdigest(), size)

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self

	def is_following(self, user):
		return self.followed.filter(
			followers.c.followed_id == user_id).count() > 0

	def followed_posts(self):
		return Post.query.join(
			followers, (followers.c.followed_id == Post.user_id)).filter(
			followers.c.followed_id == self.id).order_by(
			Post.timestamp.desc())

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
	user_id = database.Column(database.Integer, database.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post %r>' % (self.body)