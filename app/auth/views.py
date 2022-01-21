from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app.database import db
from app.extensions import login_manager

from .forms import LoginForm, RegisterForm
from .models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(user_id)


@bp.route("/register", methods=("GET", "POST"))
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(
            "Thank you for registering. You've now unlocked some new features!",
            "success",
        )
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        login_user(form.user)
        flash("You are logged in.", "success")
        return redirect(url_for("main.index"))

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("main.index"))
