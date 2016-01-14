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