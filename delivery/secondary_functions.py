from babel import dates

from delivery.models import db, Meal


def meals_in_cart_list(cart):
    meals_in_cart = []
    for item in set(cart):
        meal = db.session.query(Meal).get(item)
        meal_item = {'id': meal.id, 'title': meal.title, 'price': meal.price, 'description': meal.description,
                     'picture': meal.picture, 'quantity': cart.count(item)}
        meal_item['sum'] = meal_item['price'] * meal_item['quantity']
        meals_in_cart.append(meal_item)
    return meals_in_cart


def date_format(datetime):
    date = dates.format_datetime(datetime, "dd MMMM", locale='ru_RU')
    return date


def case_endings(length):
    if len in [i for i in range(5, 21)]:
        return 'блюд'
    elif length % 10 == 1:
        return 'блюдо'
    elif length % 10 == 2 or length % 10 == 3 or length % 10 == 4:
        return 'блюда'
    else:
        return 'блюд'
