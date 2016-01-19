from web import app
from web import database
from web.domain.entities import User

class UserVm(object):
	def Get(self, id):
		return User.query.get(int(id))
