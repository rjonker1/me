from flask import Flask, render_template, flash, redirect, url_for, g
from flask.ext.wtf import Form
from flask.ext.login import LoginManager, login_user, logout_user, current_user
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from datetime import datetime

from web import app, database, domain_entities
from web.oauth import OAuthSignIn
from web.forms import LoginForm
#from oauth import OAuthSignIn


class Login(Form):

	def CurrentUser(self):		
		#g.user = current_user
		#until login is sorted
		user = domain_entities.User.query.get(int(1))		
		current_user = user
		# if current_user is None:
		# 	login_user(user, True) 
		g.user = current_user
		if g.user.is_authenticated:
			g.user.last_seen = datetime.utcnow()
			database.session.add(g.user)
			database.session.commit()
	
	def Get(self):
		form = LoginForm()
		if form.validate_on_submit():
			flash('Login requested for Social Id="%s", remember_me=%s' % (self.socialid.data, str(self.remember_me.data)))
			return redirect('/')

		return render_template('login.htm', title='Sign In', form=self, providers=app.config['OPENID_PROVIDERS'])

	def Logout(self):
		logout_user()
		return redirect('/')

	def Authorize(self, provider):
		if not current_user.is_anonymous:
			redirect('/')
		oauth = OAuthSignIn.get_provider(provider)
		return oauth.authorize()

	def CallBack(self, provider):
		if not current_user.is_anonymous:
			redirect('/')
		oauth = OAuthSignIn.get_provider(provider)
		social_id, username, email = oauth.callback()
		if social_id is None:
			flash('Authentication Failed')
			return redirect('/')
		user = domain_entities.User.query.filter_by(social_id=social_id).first()
		if not user:
			user = domain_entities.User(social_id=social_id, nickname=username, email=email)
			database.session.add(user)
			database.session.commit()
		login_user(user, True)
		return redirect('/')