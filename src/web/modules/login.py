from flask import Flask, render_template, flash, redirect, url_for
from flask.ext.wtf import Form
from flask.ext.login import LoginManager, login_user, logout_user, current_user
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

from web import app
from web import database
from web.oauth import OAuthSignIn
#from oauth import OAuthSignIn


class LoginForm(Form):
	"""Login Form"""
	openid = StringField('openid', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)
	
	def Get(self):
		if self.validate_on_submit():
			flash('Login requested for OpenID="%s", remember_me=%s' % (self.openid.data, str(self.remember_me.data)))
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
		user = User.query.filter_by(social_id=social_id).first()
		if not user:
			user = User(social_id=social_id, nickname=username, email=email)
			database.session.add(user)
			database.session.commit()
		login_user(user, True)
		return redirect('/')