import os
import sys
import unittest

sys.path.append('../')

from config import basedirectory
from web import app, database
from web.domain.entities import User

class when_creating_profile(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedirectory, 'database/testapp.db')
		self.app = app.test_client()
		database.create_all()

	def tearDown(self):
		database.session.remove()
		database.drop_all()

	def test_then_avatar_should_exist(self):
		user = User(nickname='tester', email='rdjnkr@gmail.com')
		avatar = user.avatar(128)
		expected = 'http://www.gravatar.com/avatar/4df786bfffbe8b7e48da084c5ea200a9?d=mm&s=128'
		assert avatar[0:len(expected)] == expected

	def test_then_nickname_must_be_unique(self):
		entered_nickname = 'tester'
		user = User(nickname=entered_nickname, email='rdjnkr@gmail.com')
		database.session.add(user)
		database.session.commit()
		nickname = User.make_unique_nickname(entered_nickname)
		assert nickname != entered_nickname
		user = User(nickname=nickname, email='rdjnkr1@gmail.com')
		database.session.add(user)
		database.session.commit()
		nickname2 = User.make_unique_nickname(entered_nickname)
		assert nickname2 != entered_nickname
		assert nickname2 != nickname

class when_following_user(unittest.TestCase):
	def setup(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedirectory, 'database/testapp.db')
		self.app = app.test_client()
		database.create_all()

	def tearDown(self):
		database.session.remove()
		database.drop_all()

	def test_then_follow_should_work(self):
		user1 = User(nickname='john', email='john@somewhere.com')
		user2 = User(nickname='susan', email='susan@example.com')
		database.session.add(user1)
		database.session.add(user2)
		database.session.commit()
		assert user1.unfollow(user2) is None

		user = user1.follow(user2)
		database.session.add(user)
		database.session.commit()

		assert user1.follow(user2) is None
		assert user1.is_following(user2)

		assert user1.followed.count() == 1
		assert user1.followed.first().nickname == 'susan'

		assert user2.followers.count() == 1
		assert user2.followers.first().nickname == 'john'

		unfollow = user1.unfollow(user2)
		assert unfollow is not None
		database.session.add(unfollow)
		database.session.commit()

		assert not user1.is_following(user2)
		assert user1.followed.count() == 0
		assert user2.followers.count() == 0


if __name__ == '__main__':
	unittest.main()