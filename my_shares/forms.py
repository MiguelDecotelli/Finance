from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, EqualTo
from my_shares.models import User
from my_shares.my_functions import apology

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder":"Username", "autocomplete": False})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder":"Password"})
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder":"Username", "autocomplete": False})
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Password must match!')], render_kw={"placeholder":"Password"})
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()], render_kw={"placeholder":"Confirm password"})
    submit = SubmitField('Register')

    def check_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            return apology('Sorry, that username is taken!')
        
class ChangePassword(FlaskForm):
    old_password = PasswordField('old_assword', validators=[DataRequired()], render_kw={"placeholder":"Current password"})
    new_password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Password must match!')], render_kw={"placeholder":"New password"})
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()], render_kw={"placeholder":"Confirm new password"})
    submit = SubmitField('Change Password')

class QuoteForm(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired()], render_kw={"placeholder":"Symbol", "autocomplete": False, "autofocus": True})
    submit = SubmitField('Quote')

class BuyForm(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired()], render_kw={"placeholder":"Symbol", "autocomplete": False, "autofocus": True})
    shares = IntegerField('Shares', validators=[DataRequired()], render_kw={"placeholder":"Shares", "min":1, "autocomplete": False})
    submit = SubmitField('Buy')

class SellForm(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired()], render_kw={"placeholder":"Symbol", "autocomplete": False, "autofocus": True})
    shares = IntegerField('Shares', validators=[DataRequired()], render_kw={"placeholder":"Shares", "min":1, "autocomplete": False})
    submit = SubmitField('Sell')


class StockListForm(FlaskForm):
    symbol_search = StringField('Symbol Search', render_kw={"placeholder":"Company's Name", "autocomplete": False, "autofocus": True})
    submit = SubmitField('Search')

class CashForm(FlaskForm):
    add_cash = FloatField('Add Cash', validators=[DataRequired()], render_kw={"placeholder":"Inform Amount", "autocomplete": False, "autofocus": True})
    add_card = StringField('Add Card', validators=[DataRequired()], render_kw={"placeholder":"Inform Credit Card Number", "autocomplete": False})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder":"Password"})
    submit = SubmitField('Add Cash')

