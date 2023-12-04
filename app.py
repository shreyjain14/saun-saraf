import sqlite3
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from user_bits import UserGold, check_for_user
from web_forms import LoginForm, AddMoney, SubMoney
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from apiResponse import get_gold_from_inr, get_inr_from_gold


app = Flask(__name__)
load_dotenv('.env')
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(min=8, max=32)],
                             render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        uname = str(username.data).lower()
        existing_user_username = User.query.filter_by(username=uname).first()
        if existing_user_username:
            return True


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', form=form, error=True)
        else:
            return render_template('login.html', form=form, error=True)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    try:
        if form.validate_username(form.username):
            return render_template('register.html', form=form, error=True)
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data.lower(), password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    except sqlite3.IntegrityError:
        return render_template('register.html', form=form, error=True)

    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    username = current_user.username

    if not check_for_user(username):
        user = UserGold(username, 0)
        user.save()

    user = UserGold(username)
    user.get()
    amount_inr = get_inr_from_gold(user.goldBits)

    return render_template('dashboard.html', user=user,
                           amount_inr=amount_inr)


@app.route('/dashboard/money/add', methods=['GET', 'POST'])
@login_required
def addMoney():
    username = current_user.username

    addFrom = AddMoney()

    if addFrom.validate_on_submit():
        amount = addFrom.amount.data
        amount_gold = get_gold_from_inr(amount)
        user = UserGold(username, 0)
        user.get()
        user.update(user.goldBits + amount_gold)
        return redirect(url_for('dashboard'))

    user = UserGold(username)
    user.get()
    amount_inr = get_inr_from_gold(user.goldBits)

    return render_template('money/add.html', user=user,
                           amount_inr=amount_inr, addFrom=addFrom)


@app.route('/dashboard/money/Withdraw', methods=['GET', 'POST'])
@login_required
def subMoney():
    username = current_user.username
    subForm = SubMoney()

    if subForm.validate_on_submit():
        amount = subForm.amount.data
        amount_gold = get_gold_from_inr(amount)
        user = UserGold(username, 0)
        user.get()
        user.update(user.goldBits - amount_gold)
        return redirect(url_for('dashboard'))

    user = UserGold(username)
    user.get()
    amount_inr = get_inr_from_gold(user.goldBits)

    return render_template('money/sub.html', user=user,
                           amount_inr=amount_inr, subForm=subForm)


if __name__ == "__main__":
    app.run()
