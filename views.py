import flask
from flask import render_template, session, redirect, url_for, flash

import forms
from models import Category, User, Order
from secondary_functions import *
from models import create_app


app = create_app()
app.app_context().push()


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
