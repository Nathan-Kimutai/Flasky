from flask import render_template,session,redirect,url_for,abort,flash
from flask_login import login_required
from . import main
from flask_login import current_user
from .forms import NameForm,EditProfileForm
from ..import db
from ..models import User,Permission
from ..decorators import admin_required,permission_required


@main.route("/",methods=['GET','POST'])
def home():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False 
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ""
        return redirect(url_for(".home"))
    return render_template("index.html",form=form,name=session.get('name'),known=session.get('known',False))

@main.route("/edit-profile",methods=["GET","POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location= form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash("Your profile has been updated")
        return redirect(url_for("main.user",username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template("edit_profile.html",form=form)


@main.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("The username does not exist")
        abort(404)
    return render_template("user.html",user=user)



@main.route("/admin")
@login_required
@admin_required
def for_admins_only():
    return  "For administrators"


