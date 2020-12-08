from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from delivery.config import Config
from delivery.models import db, migrate, Category, Meal, User, Order

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
admin = Admin(app)


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Meal, db.session))

from delivery.views import *


if __name__ == '__main__':
    app.run(debug=True)
