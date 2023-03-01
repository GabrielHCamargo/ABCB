from flask import render_template, redirect, flash
from flask_login import login_user, logout_user, login_required
from app import app, login_manager

from app.models.forms import LoginForm

from app.models.default import Default


@login_manager.user_loader
def load_user(id):
    return Default.fetch_user(id)


@app.route("/index")
@app.route("/")
def index():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Default.user_validation(form.username.data, form)
        if user:
            login_user(user)
            return redirect("/dashboard")
        else:
            flash("Invalid login.")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect("/login")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/records")
@login_required
def records():
    return render_template("records.html")


@app.route("/default")
def default():
    from app.models.tables import Codes, Users
    from app import db
    import pandas as pd
    import os, secrets

    users = [
        Users(secrets.token_hex(16), "operador", 'operador2023', "Operador", "admin", 151, "activated"),
        Users(secrets.token_hex(16), "igor", 'Yeshua8293', "Igor", "admin", 151, "activated"),
        Users(secrets.token_hex(16), "anderson", 'a1b2c3d4', "Anderson", "admin", 151, "activated"),
    ]
    try:
        for u in users:
            db.session.add(u)
        
        db.session.commit()
    except:
        db.session.rollback()

    file = pd.read_excel(os.path.join(app.config["BASE_DIR"], "app", "static", "upload", "DATA", "Codes.xlsx"))

    list_data = []
    for index, line in file.iterrows():
        list_data.append(
            {
                "operation": line["Operation"],
                "result": line["Result"],
                "error": "{:0>3}".format(int(line["Error"])),
                "description": line["Description"],
                "status": line["Status"],
            }
        )

    try:
        for i in list_data:
            i = Codes(**i)
            db.session.add(i)
            db.session.commit()
    except:
        db.session.rollback()
    
    db.session.rollback()
    return redirect("/login")