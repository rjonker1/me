from flask import render_template
from flask.ext.login import login_required
from web import app, loginManager, database, modules_index, modules_login, modules_profile, vm_userviewmodel


@loginManager.user_loader
def load_user(id):
	return vm_userviewmodel.UserVm.Get(id)

@app.before_request
def before_request():
	modules_login.Login().CurrentUser()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	database.session.rollback()
	return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
#@login_required
def index(page=1):
	return modules_index.Index().Get(page)

@app.route('/login', methods=['GET', 'POST'])
def login():
	return modules_login.Login().Get()

@app.route('/logout')
def logout():
	return modules_login.Login().Logout()

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
	return modules_login.Login().Authorize(provider)

@app.route('/callback/<provider>')
def oauth_callback(provider):
	return modules_login.Login().CallBack(provider)

@app.route('/user/<nickname>', endpoint="user")
@app.route('/user/<nickname>/<int:page>')
#@login_required
def user(nickname, page=1):
	return modules_profile.Profile().Get(nickname)

@app.route('/user/edit', methods=['GET', 'POST'], endpoint="user-edit")
#@login_required
def useredit():
	return modules_profile.Profile().Edit()