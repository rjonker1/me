from flask import render_template
from web.fakes import data #fake data for testing

class Index():
	"""Index Module"""
	def Get(self):
		status = '200 OK'
		return render_template('index.htm', title='Home', user = data.user, posts = data.posts)
