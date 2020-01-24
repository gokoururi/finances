from finances import db
from finances.models import *

class ExpenditureObj:
    def __init__(self, id):
        exp = Expenditure.query.filter(Expenditure.id==id).first()
        self.id = exp.id
        self.title = exp.title
        self.price = exp.price
        self.payed = exp.payed

    def get(self):
        return {'id': self.id,
                'title': self.title,
                'price': '%0.2f' % self.price,
                'payed': self.payed}


class BudgetObj:
    def __init__(self, id):
        budget = Budget.query.filter(Budget.id==id).first()
        self.id = budget.id
        self.title = budget.title
        if budget.budget:
            self.budget = budget.budget
        else:
            self.budget = 0
        self.closed = budget.closed
        self.expenditures = self.getExps()

    def leftover(self):
        value = self.budget
        for exp in self.expenditures:
            if exp.payed:
                value = value - exp.price
        return round(value, 2)

    def plannedLeftover(self):
        value = self.budget
        for exp in self.expenditures:
            value = value - exp.price
        return round(value, 2)

    def spendings(self):
        value = 0
        for exp in self.expenditures:
            if exp.payed:
                value = value + exp.price
        return round(value, 2)

    def plannedSpendings(self):
        value = 0
        for exp in self.expenditures:
             value = value + exp.price
        return round(value, 2)

    def getExps(self):
        exps = []
        for exp in Expenditure.query.filter(Expenditure.budget_id==self.id):
            exps.append(ExpenditureObj(exp.id))
        return exps

    def getObjDicts(self, object):
        objArray = []
        for obj in object:
            objArray.append(obj.get())
        return objArray

    def get(self):
        return {'id': self.id,
                'title': self.title,
                'budget': '%0.2f' % self.budget,
                'closed': self.closed,
                'leftover': '%0.2f' % self.leftover(),
                'plannedLeftover': '%0.2f' % self.plannedLeftover(),
                'spendings': '%0.2f' % self.spendings(),
                'plannedSpendings': '%0.2f' % self.plannedSpendings(),
                'expenditures': self.getObjDicts(self.expenditures)}


class TermObj:
    def __init__(self, id):
        term = Term.query.filter(Term.id==id).first()
        self.id = term.id
        self.title = term.title
        self.income = term.income
        self.budgets = self.getBudgets()
        self.linked = False
        linkedTerm = Termlink.query.filter(Termlink.id==id).first()
        if linkedTerm:
            self.linked = True
            self.linkedTerm = TermObj(linkedTerm.linkedterm)

    def getBudgets(self):
        budgets = []
        for budget in Budget.query.filter(Budget.term_id==self.id):
            budgets.append(BudgetObj(budget.id))
        return budgets

    def getObjDicts(self, object):
        objArray = []
        for obj in object:
            objArray.append(obj.get())
        return objArray

    def leftover(self):
        value = self.income
        for budget in self.budgets:
            value = value - budget.spendings()
        if self.linked:
            value = value + self.linkedTerm.leftover()
        return value

    def plannedLeftover(self):
        value = self.income
        for budget in self.budgets:
            if budget.budget >= budget.plannedSpendings() and not budget.closed:
                value = value - budget.budget
            else:
                value = value - budget.plannedSpendings()
        if self.linked:
            value = value + self.linkedTerm.plannedLeftover()
        return value

    def spendings(self):
        value = 0
        for budget in self.budgets:
            value = value + budget.spendings()
        return value

    def plannedSpendings(self):
        value = 0
        for budget in self.budgets:
            if budget.budget >= budget.plannedSpendings() and not budget.closed:
                value = value + budget.budget
            else:
                value = value + budget.plannedSpendings()
        return value

    def get(self):
        return {'id': self.id,
                'title': self.title,
                'income': '%0.2f' % self.income,
                'leftover': '%0.2f' % self.leftover(),
                'plannedLeftover': '%0.2f' % self.plannedLeftover(),
                'spendings': '%0.2f' % self.spendings(),
                'plannedSpendings': '%0.2f' % self.plannedSpendings(),
                'budgets': self.getObjDicts(self.budgets),
                'linked': self.linked}
