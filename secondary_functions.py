import locale

from models import db, Meal


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
