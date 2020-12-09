from flask import Flask
from flask_admin import Admin

from delivery.config import Config
from delivery.models import db, migrate, Category, Meal, User, Order

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
admin = Admin(app)

from delivery.views import *
from delivery.admin import *


if __name__ == '__main__':
    app.run(debug=False)
