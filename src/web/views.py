from flask import render_template
from flask.ext.login import login_required

from web import app, loginManager
from web import database
from web.modules.index import Index
from web.modules.login import Login
from web.modules.profile import Profile
from web.view_models.userviewmodel import UserVm

@loginManager.user_loader
def load_user(id):
	return UserVm.Get(id)

@app.before_request
def before_request():
	Login().CurrentUser()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	database.session.rollback()
	return render_template('500.html'), 500

@app.route('/')
@app.route('/rudijonker')
#@login_required
def index():
	return Index().Get()

@app.route('/login', methods=['GET', 'POST'])
def login():
	return Login().Get()

@app.route('/logout')
def logout():
	return Login().Logout()

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
	return Login().Authorize(provider)

@app.route('/callback/<provider>')
def oauth_callback(provider):
	return Login().CallBack(provider)

@app.route('/user/<nickname>', endpoint="user")
#@login_required
def user(nickname):
	return Profile().Get(nickname)

@app.route('/user/edit', methods=['GET', 'POST'], endpoint="user-edit")
#@login_required
def useredit():
	return Profile().Edit()