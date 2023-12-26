import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_

import json

from models import Publisher, Book, Shop, Stock, Sale, create_tables
from settings import db_user_name, db_pass_user, db_name

# подключение к БД
DSN = 'postgresql://%s:%s@localhost:5432/%s' % (db_user_name, db_pass_user, db_name)
engine = sqlalchemy.create_engine(DSN)

# создание таблиц в БД
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# чтение и загрузка данных
with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

# прием имени или id издателя
pub_input = input(f'Введите id или имя издателя: ')
query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale)
if pub_input.isnumeric():
    query = query.filter(Publisher.id == pub_input).all()
else:
    query = query.filter(Publisher.name == pub_input).all()
for title, name, price, date_sale in query:
    print(f"{title} | {name} | {price} | {date_sale}")


session.close()
