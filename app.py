import locale

import flask
from flask import Flask, render_template, session, redirect, url_for, flash

import forms
from config import Config
from models import db, migrate, Category, Meal, User, Order
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
admin = Admin(app)


def meals_(cart):
    meals_in_cart = []
    for item in set(cart):
        meal = db.session.query(Meal).get(item)
        meal_item = {'id': meal.id, 'title': meal.title, 'price': meal.price, 'description': meal.description,
                     'picture': meal.picture, 'quantity': cart.count(item)}
        meal_item['sum'] = meal_item['price'] * meal_item['quantity']
        meals_in_cart.append(meal_item)
    return meals_in_cart


def date_format(datetime):
    locale.setlocale(locale.LC_ALL, "ru")
    date = datetime.strftime('%d %B').split(" ")
    if date[1] == 'Март' or date[1] == 'Август':
        date[1] = date[1] + 'а'
    else:
        date[1] = date[1][:-1] + 'я'
    return ' '.join(date)


def case_endings(len):
    if len in [i for i in range(5, 21)]:
        return 'блюд'
    elif len % 10 == 1:
        return 'блюдо'
    elif len % 10 == 2 or len % 10 == 3 or len % 10 == 4:
        return 'блюда'
    else:
        return 'блюд'


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Meal, db.session))


@app.route('/')
def main_view():
    cart = session.get("cart", [])
    meals_in_cart = meals_(cart)
    dish = case_endings(len(meals_in_cart))
    user = session.get("user")
    if user is None:
        is_login = False
    else:
        is_login = True
    meals = dict()
    for category in db.session.query(Category).all():
        meals[category.title] = []
        for meal in db.session.query(Meal).filter_by(category_id=category.id).order_by(db.func.random()).limit(3).all():
            meals[category.title].append(
                {'id': meal.id, 'title': meal.title, 'price': meal.price, 'description': meal.description, 'picture': meal.picture}
            )
    return render_template("main.html", meals=meals, cart=cart, meals_in_cart=meals_in_cart, is_login=is_login, dish=dish)


@app.route('/addtocart/<int:meal_id>/')
def addtocart_view(meal_id):
    cart = session.get("cart", [])
    cart.append(meal_id)
    session['cart'] = cart
    return redirect('/cart/')


@app.route('/removefromcart/<int:meal_id>/')
def removefromcart_view(meal_id):
    cart = session['cart']
    cart.remove(meal_id)
    session['cart'] = cart
    flash("Блюдо удалено из корзины")
    return redirect('/cart/')


@app.route('/cart/', methods=["POST", "GET"])
def cart_view():
    form = forms.OrderForm()
    cart = session.get("cart", [])
    meals_in_cart = meals_(cart)
    dish = case_endings(len(meals_in_cart))
    user = session.get("user")
    if user is None:
        is_login = False
    else:
        is_login = True
        form.mail.data = user
    if flask.request.method == 'GET':
        return render_template("cart.html", cart=cart, meals_in_cart=meals_in_cart, is_login=is_login, form=form, dish=dish)
    if form.validate_on_submit():
        order = Order(
            price=form.order_summ.data,
            status="Принят",
            user=db.session.query(User).filter_by(mail=user).first(),
            phone=form.phone.data,
            address=form.address.data,
            meals=[db.session.query(Meal).get(i) for i in cart],
            cart=','.join([str(i) for i in cart])
        )
        db.session.add(order)
        db.session.commit()
        return redirect(url_for("order_view"))
    return render_template("cart.html", cart=cart, meals_in_cart=meals_in_cart, is_login=is_login, form=form, dish=dish)


@app.route('/account/')
def account_view():
    cart = session.get("cart", [])
    meals_in_cart = meals_(cart)
    dish = case_endings(len(meals_in_cart))
    user = session.get("user")
    if user is None:
        is_login = False
    else:
        is_login = True
    user_id = db.session.query(User).filter(User.mail == user).first()
    orders = []
    for order in db.session.query(Order).filter(Order.user == user_id).all():
        date = date_format(order.datetime)
        meals = meals_([int(i) for i in order.cart.split(",")])
        orders.append({"date": date, "sum": order.price, "status": order.status, "meals": meals})
    return render_template("account.html", meals_in_cart=meals_in_cart, is_login=is_login, orders=orders, dish=dish)


@app.route('/auth/', methods=["POST", "GET"])
def login_view():
    form = forms.AuthenticationForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.mail == form.mail.data).first()
        if user and user.password_valid(form.password.data):
            session["user"] = form.mail.data
            return redirect(url_for("account_view"))
        else:
            form.password.errors.append("Неправильный пароль")
            return render_template("auth.html", form=form)
    return render_template("auth.html", form=form)


@app.route('/register/', methods=["POST", "GET"])
def register_view():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        mail = form.mail.data
        password = form.password.data
        user = User(mail=mail, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = mail
        return redirect((url_for('main_view')))
    return render_template("register.html", form=form)


@app.route('/logout/')
def logout_view():
    session.clear()
    return redirect(url_for("login_view"))


@app.route('/ordered/')
def order_view():
    session.pop("cart", [])
    return render_template("ordered.html")


if __name__ == '__main__':
    app.run(debug=True)
