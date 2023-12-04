from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(min=8, max=32)],
                             render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


class AddMoney(FlaskForm):
    amount = IntegerField(validators=[InputRequired()])

    submit = SubmitField('Add Money (INR)')


class SubMoney(FlaskForm):
    amount = IntegerField(validators=[InputRequired()])

    submit = SubmitField('Subtract Money (INR)')
