from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore

from delivery import admin
from delivery.models import *
from delivery import app

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Meal, db.session))


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
