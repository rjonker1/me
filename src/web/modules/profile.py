from flask import Flask, render_template, flash, redirect, url_for, session, request, g
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from datetime import datetime

from web import app
from web import database
from web.domain.entities import User, Post

from web.forms import EditForm


class Profile(object):

	def Get(self, nickname):
		user = User.query.filter_by(nickname=nickname).first()
		if user is None:
			flash('User %s not found' % nickname)
			return redirect('/')
		posts = [
		{'author': user, 'body': 'Post #1'},
		{'author': user, 'body': 'Post #2'}
		]
		return render_template('user.htm', user=user, posts=posts)

	def Edit(self):
		form = EditForm(g.user.nickname)
		if form.validate_on_submit():
			g.user.nickname = form.nickname.data
			g.user.about_me = form.about_me.data
			database.session.add(g.user)
			database.session.commit()
			flash('Changes have been saved')
			return redirect(url_for('user-edit'))
		else:
			form.nickname.data = g.user.nickname
			form.about_me.data = g.user.about_me
		return render_template('user-edit.htm', form=form)