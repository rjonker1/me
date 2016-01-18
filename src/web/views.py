from web import app
from web.modules.index import Index
from web.modules.login import LoginForm


@app.route('/')
@app.route('/rudijonker')
def index():
	return Index().Get()

@app.route('/login', methods=['GET', 'POST'])
def login():
	return LoginForm().Get()

@app.route('/logout')
def logout():
	return LoginForm().Logout()

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
	return LoginForm().Authorize(provider)

@app.route('/callback/<provider>')
def oauth_callback(provider):
	return LoginForm().CallBack(provider)