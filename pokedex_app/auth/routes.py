from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user

from pokedex_app.models import User
from pokedex_app.auth.forms import SignUpForm, LoginForm

from pokedex_app import bcrypt
from pokedex_app import db

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash("New account succesfully added.")
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)  # TODO: Check cookie

            return redirect(request.args.get('next') or url_for('main.homepage'))

    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))
