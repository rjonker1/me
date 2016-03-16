from flask import render_template, flash, redirect, session, url_for, request, g
from web.fakes import data #fake data for testing
from web import app, database, domain_entities
from web.forms import LoginForm, EditForm, PostForm
from config import POSTS_PER_PAGE
from datetime import datetime

class Index():
	"""Index Module"""
	def Get(self, page=1):
		status = '200 OK'
		form = PostForm()
		if form.validate_on_submit():
			post = domain_entities.Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)
			database.session.add(post)
			database.session.commit()
			flash('Post is live')
			return redirect(url_for('index'))
		posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
		return render_template('index.htm', title='Home', form=form, posts=posts)