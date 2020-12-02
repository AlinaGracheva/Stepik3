from flask import Flask, render_template, session, redirect
from models import db, migrate, Category, Meal
from config import Config
import forms
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)

@app.route('/')
def main_view():
    if type(session["cart"]) is int or session.get("cart") is None:
        session["cart"] = []
    cart = session["cart"]
    meals_in_cart = []
    for item in set(cart):
        meal = db.session.query(Meal).get(item)
        meal_item = {'id': meal.id, 'title': meal.title, 'price': meal.price, 'description': meal.description,
                     'picture': meal.picture, 'quantity': cart.count(item)}
        meal_item['sum'] = meal_item['price'] * meal_item['quantity']
        meals_in_cart.append(meal_item)
    user = session.get("user")
    if user is None:
        is_login = False
    meals = dict()
    for category in db.session.query(Category).all():
        meals[category.title] = []
        for meal in db.session.query(Meal).filter_by(category_id=category.id).order_by(db.func.random()).limit(3).all():
            meals[category.title].append(
                {'id': meal.id, 'title': meal.title, 'price': meal.price, 'description': meal.description, 'picture': meal.picture})
    return render_template("main.html", meals=meals, cart=cart, meals_in_cart=meals_in_cart, is_login=is_login)


@app.route('/addtocart/<int:meal_id>/')
def addtocart_view(meal_id):
    if type(session["cart"]) is int or session.get("cart") is None:
        session["cart"] = []
    cart = session["cart"]
    cart.append(meal_id)
    session['cart'] = cart
    return redirect('/cart/')


@app.route('/cart/')
def cart_view():
    form = forms.OrderForm()
    cart = session["cart"]
    meals_in_cart = []
    for item in set(cart):
        meal = db.session.query(Meal).get(item)
        meal_item = {'id': meal.id, 'title': meal.title, 'price': meal.price, 'description': meal.description,
                     'picture': meal.picture, 'quantity': cart.count(item)}
        meal_item['sum'] = meal_item['price'] * meal_item['quantity']
        meals_in_cart.append(meal_item)
    user = session.get("user")
    if user is None:
        is_login = False

    return render_template("cart.html", cart=cart, meals_in_cart=meals_in_cart, is_login=is_login, form=form)


@app.route('/account/')
def account_view():
    return render_template("account.html")


@app.route('/auth/')
def login_view():
    return render_template("login.html")


@app.route('/register/')
def register_view():
    return render_template("register.html")


@app.route('/logout/')
def logout_view():
    return 'Hello World!'


@app.route('/ordered/')
def order_view():
    return render_template("ordered.html")


if __name__ == '__main__':
    app.run(debug=True)
