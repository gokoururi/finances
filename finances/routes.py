from flask import render_template, url_for, flash, redirect, request, jsonify
from finances import app, db
from finances.models import Term, Termlink, Budgettemplate, Budget, Expenditure
from finances.forms import *
from finances.data import *

@app.route("/_modTerm")
def modTerm():
    title = request.args.get('title', 'None', type=str)
    income = request.args.get('income', 'None', type=float)
    termId = request.args.get('termid', type=int)

    term = Term.query.filter(Term.id==termId)
    term.update({'title': title,
                 'income': income})
    db.session.commit()
    return jsonify({"result": termId})

@app.route('/_removeExp/<int:expId>')
def removeExp(expId):
    Expenditure.query.filter(Expenditure.id==expId).delete()
    db.session.commit()
    return jsonify({"result": "deleted"})

@app.route('/_modExp')
def modExp():
    title = request.args.get('title', 'None', type=str)
    price = request.args.get('price', 0, type=float)
    payed = request.args.get('payed', False, type=str)
    expId = request.args.get('expenditureid', type=int)

    if payed == 'true':
        payed = True
    else:
        payed = False

    expenditure = Expenditure.query.filter(Expenditure.id==expId)
    expenditure.update({'title': title,
                        'price': price,
                        'payed': payed})
    db.session.commit()
    return jsonify({"result": expId})

@app.route('/_addExp')
def addExp():
    title = request.args.get('title', 'None', type=str)
    price = request.args.get('price', 0, type=float)
    payed = request.args.get('payed', False, type=str)
    budgetid = request.args.get('budgetid', type=int)

    if payed == 'true':
        payed = True
    else:
        payed = False

    newExpenditure = Expenditure(title=title,
                                 price=price,
                                 payed=payed,
                                 budget_id=budgetid)

    db.session.add(newExpenditure)
    db.session.commit()
    return jsonify({"result": "ok"})

@app.route('/_budgetData')
def budget_data():
    id = request.args.get('id', 2, type=int)
    budget = BudgetObj(id).get()
    return jsonify(budget)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route("/jquery")
def jquery():
    return render_template('jquery.html', title="JQuery Test")

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title="Home")

@app.route("/fixedcosts")
def fixedcosts():
    return render_template('fixedcosts.html', title="Fixed Costs")

@app.route("/addbudget", methods=['POST'])
def addbudget():
    form = BudgetAddForm()
    bt = Budgettemplate.query.filter(Budgettemplate.id==form.budgettemplateid.data).first()
    newBudget = Budget(title=bt.title, budget=bt.budget,
                       term_id=form.termid.data)
    db.session.add(newBudget)
    db.session.commit()
    return redirect(request.referrer)

@app.route("/editbudget", methods=['POST'])
def editbudget():
    form = BudgetModifyForm()
    budget = Budget.query.filter(Budget.id==form.id.data)
    budget.update({'title': form.title.data,
                   'budget': form.budget.data,
                   'closed': form.closed.data})
    db.session.commit()
    return redirect(request.referrer)

@app.route("/deletebudget", methods=['POST'])
def deletebudget():
    form = BudgetDeleteForm()
    Expenditure.query.filter(Expenditure.budget_id==form.id.data).delete()
    Budget.query.filter(Budget.id==form.id.data).delete()
    db.session.commit()
    return redirect(request.referrer)

@app.route("/addterm", methods=['POST'])
def addterm():
    form = TermAddForm()
    newTerm = Term(title=form.title.data,
                   income=form.income.data)
    db.session.add(newTerm)
    db.session.commit()
    return redirect(request.referrer)

@app.route("/deleteTerm/<int:termId>")
def deleteTerm(termId):
    term = Term.query.filter(Term.id==termId).first()
    budgets = Budget.query.filter(Budget.term_id==termId)
    for budget in budgets:
        expenditures = Expenditure.query.filter(Expenditure.budget_id==budget.id)
        for expenditure in expenditures:
            Expenditure.query.filter(Expenditure.id==expenditure.id).delete()
            db.session.commit()
        Budget.query.filter(Budget.id==budget.id).delete()
        db.session.commit()
    Term.query.filter(Term.id==termId).delete()
    db.session.commit()
    return jsonify({"result": "Deleted Term " + str(termId) + ", budgets and expenditures."})

@app.route("/copyterm", methods=['POST'])
def copyterm():
    form = TermCopyForm()
    oldTerm = Term.query.filter(Term.id==form.id.data).first()
    newTerm = Term(title=oldTerm.title,
                 income=oldTerm.income)
    db.session.add(newTerm)
    db.session.flush()

    oldBudgets = Budget.query.filter(Budget.term_id==oldTerm.id)
    for oldBudget in oldBudgets:
        newBudget = Budget(title=oldBudget.title,
                           budget=oldBudget.budget,
                           closed=oldBudget.closed,
                           term_id=newTerm.id)
        db.session.add(newBudget)
        db.session.flush()

        oldExps = Expenditure.query.filter(Expenditure.budget_id==oldBudget.id)
        for oldExp in oldExps:
            newExp = Expenditure(title=oldExp.title,
                                 price=oldExp.price,
                                 payed=oldExp.payed,
                                 budget_id=newBudget.id)
            db.session.add(newExp)
    db.session.commit()
    return redirect(request.referrer)

@app.route("/modifyterm", methods=['POST'])
def modifyterm():
    form = TermModifyForm()
    term = Term.query.filter(Term.id==form.id.data)
    term.update({'income': form.income.data})
    db.session.commit()
    return redirect(request.referrer)

@app.route("/api/linkterm/<int:targetid>/<int:sourceid>", methods=['GET'])
def api_link_term(targetid, sourceid):
    try:
        targetid = request.view_args['targetid']
        sourceid = request.view_args['sourceid']
    except KeyError:
        return jsonify({"Status": "failed to read parameters"})

    if targetid == sourceid:
        return jsonify({"Status": "Link aborted. Cannot link term to itself"})

    termlinkQuery = Termlink.query.filter(Termlink.id==targetid)
    termlink = termlinkQuery.first()
    if termlink:
        termlinkQuery.update({'linkedterm': sourceid})
        db.session.commit()
        return jsonify({"Status": "Link updated"})
    else:
        newTermlink = Termlink(id=targetid, linkedterm=sourceid)
        db.session.add(newTermlink)
        db.session.commit()
        return jsonify({"Status": "Link created"})

@app.route("/api/linkterm/<int:targetid>", methods=['DELETE'])
def api_link_term_delete(targetid):
    try:
        targetid = request.view_args['targetid']
    except KeyError:
        return jsonify({"Status": "failed to read parameters"})

    termlinkQuery = Termlink.query.filter(Termlink.id==targetid)
    if termlinkQuery.first():
        termlinkQuery.delete()
        db.session.commit()
        return jsonify({"Status": "Link deleted"})
    else:
        return jsonify({"Status": "Link not found"})


@app.route("/api/term/<int:id>", methods=['GET'])
def api_term(id):
    try:
        termid = request.view_args['id']
    except KeyError:
        return jsonify({"Status": "Failed to read parameters"}), 400

    if Term.query.filter(Term.id==termid).first():
        return jsonify(TermObj(termid).get())
    else:
        return jsonify({"Status": f"Term with id '{id}' not found"}), 404


@app.route('/backend/term/<int:id>', methods=['GET'])
def backend_term(id):
    try:
        termid = request.view_args['id']
    except KeyError:
        return jsonify({"Status": "Failed to read parameters"}), 400

    return render_template('term_new.html', title='Term New', termid=termid)


@app.route("/term")
def term_list():
    terms = Term.query.all()
    return render_template('term_list.html', title='Term List', terms=terms)


@app.route("/term/<int:id>", methods=['GET'])
def term(id=False):
    try:
        req_term = request.view_args['id']
    except KeyError:
        req_term = Term.query.first().id

    expModifyForm = ExpModifyForm()
    expDeleteForm = ExpDeleteForm()
    budgetAddForm = BudgetAddForm()
    budgetModifyForm = BudgetModifyForm()
    budgetDeleteForm = BudgetDeleteForm()
    termAddForm = TermAddForm()
    termModifyForm = TermModifyForm()
    termCopyForm = TermCopyForm()

    budgetTupels = []
    for bt in Budgettemplate.query.all():
        budgetTupels.append((bt.id, '{} [{}]'.format(bt.title, bt.budget)))
    budgetAddForm.budgettemplateid.choices = budgetTupels

    data = TermObj(req_term).get()

    return render_template('term.html', title='Term', data=data,
                           expModifyForm=expModifyForm,
                           expDeleteForm=expDeleteForm,
                           budgetAddForm=budgetAddForm,
                           budgetModifyForm=budgetModifyForm,
                           budgetDeleteForm=budgetDeleteForm,
                           termAddForm=termAddForm,
                           termModifyForm=termModifyForm,
                           termCopyForm=termCopyForm)
