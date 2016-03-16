from web import app, database, domain_entities

class UserVm(object):
	def Get(self, id):
		return domain_entities.User.query.get(int(id))
