from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, BooleanField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class ExpModifyForm(FlaskForm):
    id = HiddenField('Id', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    payed = BooleanField('Payed')
    submit = SubmitField('Save')

class ExpDeleteForm(FlaskForm):
    id = HiddenField('Id', validators=[DataRequired()])
    submit = SubmitField('Delete')

class BudgetAddForm(FlaskForm):
    termid = HiddenField('termid', validators=[DataRequired()])
    budgettemplateid = SelectField('Id', choices=[], validators=[DataRequired()])
    submit = SubmitField('Add')

class BudgetModifyForm(FlaskForm):
    id = HiddenField('budgetid', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    budget = DecimalField('Price', validators=[DataRequired()])
    closed = BooleanField('Payed')
    submit = SubmitField('Save')

class BudgetDeleteForm(FlaskForm):
    id = HiddenField('budgetid', validators=[DataRequired()])
    submit = SubmitField('Save')

class TermAddForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    income = DecimalField('Income', validators=[DataRequired()])
    submit = SubmitField('Add')

class TermModifyForm(FlaskForm):
    id = HiddenField('id', validators=[DataRequired()])
    income = DecimalField('Income', validators=[DataRequired()])

class TermCopyForm(FlaskForm):
    id = HiddenField('id', validators=[DataRequired()])
    submit = SubmitField('Copy')
