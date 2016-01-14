from flask import render_template, flash, redirect
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from web import app

class LoginForm(Form):
	"""LoginForm"""
	openid = StringField('openid', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)
	
	def Get(self):
		if self.validate_on_submit():
			flash('Login requested for OpenID="%s", remember_me=%s' % (self.openid.data, str(self.remember_me.data)))
			return redirect('/')

		return render_template('login.htm', title='Sign In', form=self, providers=app.config['OPENID_PROVIDERS'])