from flask import Flask, render_template, session, redirect
from models import db, migrate, Category, Meal
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)

@app.route('/')
def main_view():
    if type(session["cart"]) is int or session.get("cart") is None:
        session["cart"] = []
    cart = session["cart"]
    meals_sum = 0
    for price in db.session.query(Meal.price).filter(Meal.id.in_(cart)).all():
        meals_sum += price[0]
    user = session.get("user")
    if user is None:
        is_login = False
    meals = dict()
    for category in db.session.query(Category).all():
        meals[category.title] = []
        for meal in db.session.query(Meal).filter_by(category_id=category.id).order_by(db.func.random()).limit(3).all():
            meals[category.title].append(
                {'id': meal.id, 'title': meal.title, 'price': meal.price, 'description': meal.description, 'picture': meal.picture})
    return render_template("main.html", meals=meals, cart=cart, sum=meals_sum, is_login=is_login)


@app.route('/addtocart/<int:meal_id>/')
def addtocart_view(meal_id):
    if type(session["cart"]) is int or session.get("cart") is None:
        session["cart"] = []
    cart = session["cart"]
    print(cart)
    cart.append(meal_id)
    session['cart'] = cart
    print(cart)
    meals_sum = 0
    for price in db.session.query(Meal.price).filter(Meal.id.in_(cart)).all():
        meals_sum += price[0]
    return redirect('/cart/')


@app.route('/cart/')
def cart_view():
    cart = session["cart"]
    meals_sum = 0
    for price in db.session.query(Meal.price).filter(Meal.id.in_(cart)).all():
        meals_sum += price[0]
    user = session.get("user")
    if user is None:
        is_login = False
    return render_template("cart.html", cart=cart, sum=meals_sum, is_login=is_login)


@app.route('/account/')
def account_view():
    return render_template("account.html")


@app.route('/login/')
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
    app.run(debug=False)
