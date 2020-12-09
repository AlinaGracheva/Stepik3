import csv
from datetime import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
migrate = Migrate()


orders_meals_association = db.Table("orders_meals",
                                    db.Column("order_id", db.Integer, db.ForeignKey("orders.id")),
                                    db.Column("meal_id", db.Integer, db.ForeignKey("meals.id")))


roles_users_association = db.Table("roles_users",
                                   db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
                                   db.Column("user_id", db.Integer, db.ForeignKey("users.id")))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)

    mail = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    orders = db.relationship("Order", back_populates="user")
    roles = db.relationship("Role", secondary=roles_users_association, back_populates="users")

    @property
    def password(self):
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    users = db.relationship("User", secondary=roles_users_association, back_populates="roles")


class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer(), primary_key=True)

    title = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("Category", back_populates="meals")
    orders = db.relationship("Order", secondary=orders_meals_association, back_populates="meals")


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)

    title = db.Column(db.String(), nullable=False)
    meals = db.relationship("Meal", back_populates="category")


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer(), primary_key=True)

    datetime = db.Column(db.DateTime, default=datetime.now)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="orders")
    phone = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    cart = db.Column(db.String(), nullable=False)
    meals = db.relationship("Meal", secondary=orders_meals_association, back_populates="orders")


if __name__ == "__main__":
    with open("categories.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        categories = []
        for row in reader:
            categories.append(Category(title=row[1]))
    del categories[0]
    db.session.add_all(categories)
    db.session.commit()
    with open("meals.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=',')
        meals = []
        for line in reader:
            meals.append(line)
    for meal in meals:
        to_insert = Meal(
            title=meal['title'],
            price=int(meal['price']),
            description=meal['description'],
            picture='pictures/' + meal['picture'],
            category=db.session.query(Category).get(int(meal['category_id']))
        )
        db.session.add(to_insert)
    db.session.commit()
