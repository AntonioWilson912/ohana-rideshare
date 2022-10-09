from flask_app import app
from flask_app.models import user
from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def login_registration_page():
    return render_template("login_registration.html")

@app.route("/register", methods=["POST"])
def register():
    if not user.User.validate_new_user(request.form):
        return redirect("/")
    password_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": password_hash
    }
    print(data)
    session["user_id"] = user.User.create_user(data)
    return redirect("/rides/dashboard")

@app.route("/login", methods=["POST"])
def login():
    data = { "email": request.form["email"], "password": request.form["password"]}
    found_user_or_none = user.User.validate_existing_user(data)
    if not found_user_or_none:
        return redirect("/")
    session["user_id"] = user.User.get_user_by_email(data).id
    return redirect("/rides/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")