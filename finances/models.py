from finances import db


class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    income = db.Column(db.Float)
    budgets = db.relationship('Budget', backref='term', lazy=True)


class Budgettemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    budget = db.Column(db.Float)


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    budget = db.Column(db.Float)
    closed = db.Column(db.Boolean, default=False)
    term_id = db.Column(db.Integer, db.ForeignKey('term.id'))
    expenditures = db.relationship('Expenditure', backref='budget', lazy=True)


class Expenditure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    price = db.Column(db.Float)
    payed = db.Column(db.Boolean)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'))


class Fixedcosttemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    price = db.Column(db.Float)
    default = db.Column(db.Boolean)


class Fixedcost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    price = db.Column(db.Float)
    payed = db.Column(db.Boolean)
    fixedcosttemplate_id = db.Column(db.Integer, db.ForeignKey('fixedcosttemplate.id'))
