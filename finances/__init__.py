from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os.path

dbPath = '/opt/data/finances.db'
app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/finances'
app.config['SECRET_KEY'] = '5dsjdsf32413ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbPath
db = SQLAlchemy(app)

from finances import routes

from finances.models import Term, Termlink, Budgettemplate, Budget, Expenditure

if not os.path.isfile(dbPath):
    data = [
        Term(title='Oktober 2018', income=3056.62),
        Budgettemplate(title='Luxus', budget=300),
        Budgettemplate(title='Einkäufe', budget=220),
        Budgettemplate(title='Tanken', budget=100),
        Budgettemplate(title='Sonstiges', budget=0),
        Budget(term_id=1, title='Luxus', budget=300),
        Expenditure(budget_id=1, title='Video Games', price=49.99, payed=False),
        Expenditure(budget_id=1, title='More Games', price=39.99, payed=False),
        Expenditure(budget_id=1, title='Kino', price=13, payed=True),
        Expenditure(budget_id=1, title='Kino Snacks', price=7.9, payed=False)
    ]
    db.create_all()
    db.session.add_all(data)
    db.session.commit()
else:
    db.create_all()
