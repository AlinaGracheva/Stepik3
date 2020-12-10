from flask_admin.contrib.sqla import ModelView

from delivery import admin
from delivery.models import *

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Meal, db.session))
