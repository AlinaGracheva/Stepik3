from flask import Flask
from models import db, migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)

@app.route('/')
def main_view():
    return 'Hello World!'


@app.route('/cart/')
def cart_view():
    return 'Hello World!'


@app.route('/account/')
def account_view():
    return 'Hello World!'


@app.route('/login/ ')
def login_view():
    return 'Hello World!'


@app.route('/register/')
def register_view():
    return 'Hello World!'


@app.route('/logout/')
def logout_view():
    return 'Hello World!'


@app.route('/ordered/')
def order_view():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
