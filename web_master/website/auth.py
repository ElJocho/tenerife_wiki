from flask import Blueprint, render_template, request, flash, redirect, url_for
import re
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_
from .python_utils.files import cleanup_image, allowed_file, ALLOWED_IMAGE_EXTENSIONS

"""Alles rund um User Account Management. Hier werden die backend-endpoints erstellt."""
auth = Blueprint("auth ", __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        password = data.get('password')
        username = data.get('username')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Login erfolgreich", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.landing_page"))
            else:
                flash("Falsches Passwort, erneut versuchen", category="error")
        else:
            flash("Keinen Nutzer mit dieser Email gefunden", category="error")
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth .login'))


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        data = request.form
        # login data
        email = data.get("email")
        username = data.get("username")
        password1 = data.get("password1")
        password2 = data.get("password2")

        # personal data
        name = data.get("name")
        vorname = data.get("vorname")

        user = User.query.filter(or_(User.username == username)).first()
        if user:
            if user.username == username:
                flash("Nutzername bereits vergeben", category="error")
        elif password1 != password2:
            flash("""Passwörter stimmen nicht überein""", category="error")
        elif not re.search("^(?=.*([A-Z]){1,})(?=.*[!@#$&*]{1,})(?=.*[0-9]{1,})(?=.*[a-z]{1,}).{8,30}$",
            password1):
            flash("""Passwort muss mindestens einen Großbuchstaben,
             eine Zahl und ein Sonderzeichen(!@#$&*) enthalten 
             sowie zwischen 8 und 30 Zeichen lang sein""", category="error")
        else:
            new_user = User(
                username=username,
                password=generate_password_hash(password1, method="sha256" ),
                vorname=vorname,
                name=name,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("""Account erfolgreich erstellt""", category="success")
            return redirect(url_for("views.landing_page"))

    return render_template("sign_up.html", user=current_user)

@auth.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    u_id = request.args.get('u_id')
    if u_id is None:
        u_id = current_user.id
    if request.method == "POST" and current_user.id == u_id:
        data = request.form
        name = data.get("name")
        vorname = data.get("vorname")
        password = data.get("password")
        profile_image = request.files.get("profileImage")

        if profile_image:
            if profile_image.filename != "" and allowed_file(profile_image.filename,
                                                          ALLOWED_IMAGE_EXTENSIONS):
                image, image_data_type = cleanup_image(profile_image)
                current_user.image = image
                current_user.image_data_type = image_data_type
        if name!="":
            current_user.name=name
        if vorname!="":
            current_user.vorname=vorname
        if password!="":
            current_user.password=generate_password_hash(password, method="sha256" )
        if re.search("^(?=.*([A-Z]){1,})(?=.*[!@#$&*]{1,})(?=.*[0-9]{1,})(?=.*[a-z]{1,}).{8,30}$", password) or password=="":
            db.session.commit()
        else:
            # todo: currently no warning message since we removed flashs
            pass
    
    return render_template(
        "profile.html",
        user=current_user,
        t_user=User.query.filter_by(id=u_id).first(),
    )