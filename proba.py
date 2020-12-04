from flask import Flask, render_template
from models import db, migrate, Category, Meal, User, Order
from config import Config
from app import meals_
import pprint
from datetime import datetime
import locale
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

cart = [1, 2, 3, 1, 1]
meals_sum = 0
for price in db.session.query(Meal.price).filter(Meal.id.in_(cart)).all():
    meals_sum += price[0]
#print(cart.count(1))

meals_in_cart = []
for item in set(cart):
    meal = db.session.query(Meal).get(item)
    meal_item = {'id': meal.id, 'title': meal.title, 'price': meal.price, 'description': meal.description, 'picture': meal.picture, 'quantity': cart.count(item)}
    meal_item['sum'] = meal_item['price'] * meal_item['quantity']
    meals_in_cart.append(meal_item)
#pprint.pprint(meals_in_cart)

#user = User(mail='a@mail.ru', password="1111")

# mail = 'a1@mail.ru'
# if db.session.query(User).filter(User.mail == mail).first():
#     print('not unique')
# else:
#     print('unique')

# @app.route('/cart/', methods=["POST", "GET"])
# def cart_view():
#     form = forms.OrderForm()
#     cart = session.get("cart", [])
#     meals_in_cart = meals_(cart)
#     item_del = session.get("del", False)
#     user = session.get("user")
#     if user is None:
#         is_login = False
#     else:
#         is_login = True
#     if flask.request.method == 'GET':
#         return render_template("cart.html", cart=cart, meals_in_cart=meals_in_cart, is_login=is_login, form=form, item_del=item_del)
#     if form.validate_on_submit():
#         return "Успешно"
#     return render_template("cart.html", cart=cart, meals_in_cart=meals_in_cart, is_login=is_login, form=form, item_del=item_del)
#
#
# @app.route('/removefromcart/<int:meal_id>/')
# def removefromcart_view(meal_id):
#     cart = session['cart']
#     cart.remove(meal_id)
#     session['cart'] = cart
#     session['del'] = True
#     return redirect('/cart/')
# date = datetime.today()
# db.session.query(User).filter_by(mail='a11@mail.ru').first()
# meals = [db.session.query(Meal).get(i) for i in cart]
mail = 'a11@mail.ru'
user = db.session.query(User).filter(User.mail == mail).first()
orders = []
locale.setlocale(locale.LC_ALL, "ru")
# for order in db.session.query(Order).filter(Order.user == user).all():
#     date = order.datetime.strftime('%d %B').split(" ")
#     if date[1] == 'Март' or date[1] == 'Август':
#         date[1] = date[1] + 'а'
#     else:
#         date[1] = date[1][:-1] + 'я'
#     date = ' '.join(date)
#     meals_id = []
#     print(order.meal_id)
#     for meal in order.meals:
#         meals_id.append(meal.id)
#     meals = meals_(meals_id)
#     print(meals_id)
#     orders.append({"date": date, "sum": order.price, "status": order.status, "meals": meals})

#pprint.pprint(orders)
cart = [1, 2, 2, 3]
order_cart = ','.join([str(i) for i in cart])
print(order_cart)
meals_id = [int(i) for i in order_cart.split(",")]
print(meals_id)