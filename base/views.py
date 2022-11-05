from flask import abort, flash, redirect, render_template, session, url_for, request

from base import app
from base.models import User, Secret, db
from base.forms import LoginForm, RegisterForm, SecretForm, SearchForm
from base.decorators import login_required


@app.route("/register", methods=["GET", "POST"])
def register():
    secret, qr = None, None
    form = RegisterForm()
    if form.validate_on_submit():
        u = User()
        db.session.add(u)
        db.session.commit()
        qr = u.qr
        secret = u.secret
    return render_template("register.html", form=form, qr=qr, secret=secret)


@app.route("/login/", methods=["GET", "POST"])
def login():
    session["logged_in"] = False
    form = LoginForm()
    if form.validate_on_submit():
        challenge = form.challenge.data
        users = User.query.all()
        for user in users:
            if user.verify_password(challenge):
                session["logged_in"] = True
                session["user"] = user.id
                return redirect(url_for("index"))
    return render_template("login.html", form=form, session=session)


@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    secrets = (
        Secret.query.order_by(Secret.created_at.desc())
        .filter(Secret.user_id == session.get("user"))
        .all()
    )
    form = SecretForm()
    if form.validate_on_submit():
        text = form.text.data
        s = Secret(user_id=session.get("user"), text=text)
        db.session.add(s)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("index.html", form=form, secrets=secrets)
