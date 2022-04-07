from flask import Blueprint, render_template, flash, \
    redirect, url_for, request, session
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordForm, ResetPasswordRequestForm, DeleteUserForm, \
    GiveAdminForm, RmAdminForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app import db
from werkzeug.urls import url_parse
from app.auth.email import send_password_reset_email

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        # flash("You are now signed in!", "success")
        return redirect(next_page)
    return render_template('auth/login.html', title='Login', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data.lower(),
            last_name=form.last_name.data.lower(),
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # flash('Congratulations, you are now a registered user!', 'success')
        return(redirect(url_for('auth.login')))
    return render_template('auth/register.html', title='Register', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    # session.clear()
    # flash("You've signed out!", "success")
    return redirect(url_for('main.index'))


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('An error occured, please try again', 'danger')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        # flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    user = User.query.order_by(User.username.asc())
    return render_template('auth/admin.html', user=user)


@auth.route('/admin/assign_admin/user<id>', methods=['GET', 'POST'])
@login_required
def give_admin(id):
    user = User.query.get(id)
    form = GiveAdminForm()
    if request.method == 'POST':
        if form.confirm.data:
            user.admin = 1
            db.session.commit()
            flash(user.username + ' is Admin now', 'success')
            return redirect(url_for('auth.admin'))
    if form.cancel.data:
        return redirect(url_for('auth.admin'))
    return render_template('auth/give_admin.html', user=user, title='Assign Admin', form=form)


@auth.route('/admin/assign_user/user<id>', methods=['GET', 'POST'])
@login_required
def rm_admin(id):
    user = User.query.get(id)
    form = RmAdminForm()
    if request.method == 'POST':
        if User.query.filter_by(admin=1).count() <= 1 and user.admin == 1:
            flash('Admin ' + user.username +
                  ' cannot be assigned to user (need at least one admin)', 'danger')
            return redirect(url_for('auth.admin'))
        if form.confirm.data:
            user.admin = 0
            db.session.commit()
            flash(user.username + ' is assigned to user rights now', 'success')
            return redirect(url_for('auth.admin'))
    if form.cancel.data:
        return redirect(url_for('auth.admin'))
    return render_template('auth/rm_admin.html', user=user, title='Assign Admin', form=form)


@auth.route('/admin/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    vehicles_by_user = Vehicle.query.filter_by(user_id=id)
    user = User.query.get(id)
    form = DeleteUserForm()
    if request.method == 'POST':
        if form.delete.data:
            if User.query.filter_by(admin=1).count() <= 1 and user.admin == 1:
                flash('Admin ' + user.username +
                      ' cannot be deleted (need at least one admin)', 'danger')
                return redirect(url_for('auth.admin'))
            else:
                for i in vehicles_by_user:
                    db.session.delete(i)

            db.session.delete(user)

            db.session.commit()
            flash('User ' + user.username +
                  ' was deleted successfuly', 'success')
            return redirect(url_for('auth.admin'))
    if form.cancel.data:
        return redirect(url_for('auth.admin'))
    return render_template('auth/delete_user.html', user=user, title='Delete User', form=form)
