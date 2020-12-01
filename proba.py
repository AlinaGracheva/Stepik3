from flask import Flask, render_template
from models import db, migrate, Category, Meal
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)

meals = dict()
for category in db.session.query(Category).all():
    meals[category.title] = []
    for meal in db.session.query(Meal).filter_by(category_id=category.id).order_by(db.func.random()).limit(3).all():
        meals[category.title].append({'id': meal.id, 'title': meal.title, 'price': meal.price, 'description': meal.description, 'picture': meal.picture})
#print(meals["Суши"][0])
#print(type(meals["Суши"][0].get("id")))

cart = [1, 2, 3]
meals_sum = 0
for price in db.session.query(Meal.price).filter(Meal.id.in_(cart)).all():
    meals_sum += price[0]
print(meals_sum)