import os
from datetime import datetime

import flask
from flask import (Blueprint, render_template, send_from_directory, redirect,
                   url_for, current_app, Response, get_flashed_messages)
from flask_login import (login_user, login_required, logout_user, current_user)
from is_safe_url import is_safe_url
from werkzeug.security import generate_password_hash, check_password_hash

from . import config, talis
from .forms import SignupForm, SigninForm
from .models import User, db

main = Blueprint("main", __name__)

BLACKLISTED_VIEWS = ("main.signout", "main.download")


def is_blacklisted(url: str) -> bool:
    for views in BLACKLISTED_VIEWS:
        if url.startswith(url_for(views)):
            return True
    return False


def redirect_dest(url: str) -> Response:
    dest_url = url_for("main.home")
    if url:
        if is_safe_url(url, allowed_hosts=('/',)) \
                and not is_blacklisted(url):
            dest_url = url
        else:
            flask.flash("Invalid redirection.", category="error")
    return redirect(dest_url)


def is_user_expired(usr_ob: User) -> bool:
    if usr_ob.ctime < datetime.utcnow() - config.expiry_duration:
        db.session.delete(usr_ob)
        db.session.commit()
        flask.flash("Your old account expired.", category="error")
        return True
    return False


@main.route('/')
def home():
    return render_template("index.html")


@main.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        flask.flash("You've already signed in.", category="info")
        return redirect(url_for("main.home"))

    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        req_user = User.query.filter_by(
            email=signup_form.email.data).first()

        if req_user and not is_user_expired(req_user):
            flask.flash("You've already signed up. Try Sign-in.",
                        category="info")
        else:
            new_user = User(
                name=signup_form.name.data,
                email=signup_form.email.data,
                password=generate_password_hash(
                    signup_form.password.data,
                    method="pbkdf2:sha256",
                    salt_length=16),
                ctime=datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.commit()
            flask.flash("New account created successfully.", category="info")
            flask.flash(
                "Every new account will be expired after "
                f"{config.expiry_duration.days} days.", category="info")

        return redirect(url_for("main.signin"))
    return render_template("signup.html", form=signup_form)


@main.route("/signin", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        flask.flash("You've already signed in.", category="info")
        return redirect(url_for("main.home"))

    signin_form = SigninForm()
    if signin_form.validate_on_submit():
        req_user = User.query.filter_by(email=signin_form.email.data).first()

        if req_user:
            if is_user_expired(req_user):
                flask.flash("Don't worry make a new account.",
                            category="error")
                return redirect(url_for("main.signup"))

            elif check_password_hash(req_user.password,
                                     signin_form.password.data):
                login_user(req_user)
                flask.flash("Signed in successfully.", category="info")
                return redirect_dest(flask.request.args.get("next"))

        flask.flash("Incorrect email or password.", category="error")

    return render_template("signin.html", form=signin_form)


@main.route("/secrets")
@login_required
def secrets():
    return render_template("secrets.html")


@main.route("/download")
@talis(content_security_policy=config.img_view_csp)
@login_required
def download():
    # Flushing unused flash messages, so that it won't disturb other pages.
    get_flashed_messages()
    return send_from_directory(
        os.path.join(current_app.instance_path, 'protected'),
        path="SecretFile.png")


@main.route("/signout")
@login_required
def signout():
    logout_user()
    flask.flash("Signed out successfully.", "info")
    return redirect(url_for("main.signin"))
