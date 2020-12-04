import phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField
from wtforms.fields.html5 import TelField
from wtforms.validators import InputRequired, Email, Length, ValidationError

from models import db, User


def unique_mail(form, field):
    if db.session.query(User).filter(User.mail == field.data).first():
        raise ValidationError('Пользователь с такой почтой уже существует')


def is_phone(form, field):
    try:
        phone = phonenumbers.parse(field.data)
        if not phonenumbers.is_valid_number(phone):
            raise ValueError("Некорректный номер телефона")
    except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
        raise ValidationError("Некорректный номер телефона, введите номер в международном формате")


def auth_mail(form, field):
    if not db.session.query(User).filter(User.mail == field.data).first():
        raise ValidationError('Пользователя с такой почтой не существует, пожалуйста, зарегистрируйтесь')


class OrderForm(FlaskForm):
    name = StringField("Ваше имя", [InputRequired(message="Поле должно быть заполнено")])
    address = StringField("Адрес", [InputRequired(message="Поле должно быть заполнено")])
    mail = StringField("Электронная почта", [InputRequired(message="Поле должно быть заполнено"), Email(message="Некорректный адрес электронной почты")], render_kw={'autofocus': True})
    phone = TelField("Телефон", [InputRequired(message="Поле должно быть заполнено"), is_phone])
    order_summ  = HiddenField()
    submit = SubmitField("Оформить заказ")


class RegisterForm(FlaskForm):
    mail = StringField("Электронная почта", [InputRequired(message="Поле должно быть заполнено"), Email(message="Некорректный адрес электронной почты"), unique_mail], render_kw={'autofocus': True})
    password = PasswordField("Пароль", [InputRequired(message="Поле должно быть заполнено"),Length(min=5, message="Пароль должен содержать минимум 5 символов")])
    submit = SubmitField("Зарегистрироваться")


class AuthenticationForm(FlaskForm):
    mail = StringField("Электронная почта", [InputRequired(message="Поле должно быть заполнено"),
                                             Email(message="Некорректный адрес электронной почты"), auth_mail],
                       render_kw={'autofocus': True})
    password = PasswordField("Пароль", [InputRequired(message="Поле должно быть заполнено"), ])
    submit = SubmitField("Войти")