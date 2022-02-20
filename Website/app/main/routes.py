from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import User
from app.main.forms import ContactForm

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index(cat=None):
    return render_template('index.html',  title='_home')


@main.route('/ContactUs', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash('Your message has been sent to our team', 'success')

        return redirect(url_for('main.contact'))
    return render_template('contact.html', title='Contact Us', form=form)


@main.route('/FindUs', methods=['GET', 'POST'])
def findUs():
    return render_template('find_us.html', title='Find Us')