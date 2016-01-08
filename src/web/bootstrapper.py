#import main
from flask import Flask
from domain import entities


app = Flask(__name__)

@app.route('/')
@app.route('/rudijonker')
def index():
    return "main age"

if __name__ == '__main__':
    app.run(debug=True)