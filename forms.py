from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, RadioField
from wtforms.fields.html5 import TelField
from wtforms.validators import InputRequired, Email


class OrderForm(FlaskForm):
    name = StringField("Ваше имя", [InputRequired(message="Поле должно быть заполнено")])
    address = StringField("Адрес", [InputRequired(message="Поле должно быть заполнено")])
    mail = StringField("Электронная почта", [InputRequired(message="Поле должно быть заполнено"), Email(message="Некорректный адрес электронной почты")], render_kw={'autofocus': True})
    phone = TelField("Телефон", [InputRequired(message="Поле должно быть заполнено")])
    order_summ  = HiddenField()
    order_cart = HiddenField()
    submit = SubmitField("Оформить заказ")
