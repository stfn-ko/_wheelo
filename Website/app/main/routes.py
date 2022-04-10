from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.main.forms import ContactForm, FAQForm, DeleteQuestionForm, \
    EditQuestionForm, PostForm, EditPostForm, TradeInForm, SellDetailsForm, CheckoutDetailsForm
from app.models import User, FAQ, Post, Vehicles, Model, Make, Trade
from sqlalchemy.sql import func, or_
from app.funcs import save_picture
from app import db

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():
    cars_for_render = Vehicles.query.order_by(Vehicles.id.asc())
    makes_for_render = Make.query.order_by(Make.make_id.asc())
    models_for_render = Model.query.order_by(Model.model_id.asc())
    posts_for_render = Post.query.order_by(Post.created_at.asc())
    return render_template('index.html', posts=posts_for_render, cars=cars_for_render, makes=makes_for_render, models=models_for_render, title='Home')


@main.route('/ContactUs', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash('Your message has been sent to our team', 'success')

        return redirect(url_for('main.contact'))
    return render_template('contact.html', title='Contact Us', form=form)


@main.route('/FAQ', methods=['GET', 'POST'])
def FAQs():
    questions_for_render = FAQ.query.order_by(FAQ.id.asc())
    form = FAQForm()
    if form.validate_on_submit():
        q = FAQ(
            name=form.name.data,
            question=form.question.data,
        )
        db.session.add(q)
        db.session.commit()
    return render_template('FAQ/questions.html', questions=questions_for_render, form=form, title='FAQ')


@main.route('/FAQ/view_all', methods=['GET', 'POST'])
def viewAllQuestions():
    question = FAQ.query.order_by(FAQ.id.asc())
    return render_template('FAQ/view_all.html', questions=question, title='view')


@main.route('/FAQ/view_all/vis<id>', methods=['GET', 'POST'])
@login_required
def changeVisibility(id):
    question = FAQ.query.get(id)
    if question.display == 1:
        question.display = 0
        db.session.commit()
        return redirect(url_for('main.FAQs'))
    if question.display == 0:
        question.display = 1
        db.session.commit()
        return redirect(url_for('main.FAQs'))
    return render_template('FAQ/questions.html')


@main.route('/FAQ/delete_question/<id>', methods=['GET', 'POST'])
@login_required
def delQuestion(id):
    question = FAQ.query.get(id)
    form = DeleteQuestionForm()
    if request.method == 'POST' and form.delete.data:
        db.session.delete(question)
        db.session.commit()
        flash('Question was deleted successfuly', 'success')
        return redirect(url_for('main.FAQs'))
    if form.cancel.data:
        return redirect(url_for('main.FAQs'))
    return render_template('FAQ/delete_question.html', question=question, title="Delete Question", form=form)


@main.route('/FAQ/edit_question/<id>', methods=['GET', 'POST'])
@login_required
def editQuestion(id):
    question = FAQ.query.get_or_404(id)
    form = EditQuestionForm()
    if request.method == 'GET':
        form.name.data = question.name
        form.question.data = question.question
        form.answer.data = question.answer
    elif request.method == 'POST':
        if form.update.data and form.validate_on_submit():
            question.name = request.form['name']
            question.question = request.form['question']
            question.answer = request.form['answer']
            db.session.commit()
            return(redirect(url_for('main.FAQs')))
        if form.cancel.data:
            return(redirect(url_for('main.FAQs')))
    return render_template('FAQ/edit_question.html',  question=question, title='Edit Question', form=form)


@main.route('/all_posts', methods=['GET', 'POST'])
def Blog():
    posts = Post.query.order_by(Post.id.asc())
    return render_template('blog/all_posts.html', posts=posts)


@main.route('/blog/post_page/<id>', methods=['GET', 'POST'])
def getPost(id):
    post = Post.query.get_or_404(id)
    return render_template('blog/post_page.html', post=post)


@main.route('/blog/new_post', methods=['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        picture = 'default.jpg'
        if form.picture.data:
            picture = save_picture(form.picture.data)
        p = Post(
            title=form.title.data,
            caption=form.caption.data,
            picture=picture,
            user_id=current_user.get_id()
        )
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('main.index'))
    if form.cancel.data:
        return redirect(url_for('main.index'))
    return render_template('blog/new_post.html', title='New Post', form=form)


@main.route('/blog/edit_post/<id>', methods=['GET', 'POST'])
@login_required
def editPost(id):
    post = Post.query.get_or_404(id)
    form = EditPostForm()
    if request.method == 'GET':
        form.title.data = post.title
        form.caption.data = post.caption
        form.picture.data = post.picture
    elif request.method == 'POST':
        if form.update.data and form.validate_on_submit():
            post.title = request.form['title']
            post.caption = request.form['caption']
            if form.picture.data:
                post.picture = save_picture(form.picture.data)
            db.session.commit()
            return(redirect(url_for('main.index')))
        if request.method == 'POST' and form.delete.data:
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('main.index'))
        if form.cancel.data:
            return(redirect(url_for('main.index')))
    return render_template('blog/edit_post.html',  post=post, title='Edit Post', form=form)


@main.route('/vehicle/<id>', methods=['GET', 'POST'])
def vehicle(id):
    vehicle_to_render = Vehicles.query.get(id)
    makes_for_render = Make.query.order_by(Make.make_id.asc())
    models_for_render = Model.query.order_by(Model.model_id.asc())
    return render_template('vehicles/car_page.html', car=vehicle_to_render, makes=makes_for_render, models=models_for_render)


@main.route('/trade-in', methods=['GET', 'POST'])
def trade_in():
    form = TradeInForm()
    #form.make.choices = Make.query.order_by(Make.make_id.asc())
    #form.model.choices = Model.query.order_by(Model.model_id.asc())
    if form.validate_on_submit():

        price = 1000  # use valuation to get price?

        make_exist = Make.query.filter_by(Make.make_name == form.make.data)
        if not make_exist:
            make_new = Make(
                make_name=form.make.data,
            )
            db.session.add(make_new)
            db.commit()

        makeId = Make.query.filter_by(Make.make_name == form.make.data)

        model_exist = Model.query.filter_by(
            Model.model_name == form.model.data)
        if not model_exist:
            model_new = Model(
                model_name=form.model.data,
            )
            db.session.add(model_new)
            db.commit()

        modId = Model.query.filter_by(Model.model_name == form.model.data)

        picture_folder = form.model.data + '_' + form.color.data + '_' + form.year.data
        form.picture_one.data.save(
            'app/static/car_pics' + picture_folder + '/1.jpg')
        form.picture_two.data.save(
            'app/static/car_pics' + picture_folder + '/2.jpg')
        form.picture_three.data.save(
            'app/static/car_pics' + picture_folder + '/3.jpg')

        car = Vehicles(
            make_id=makeId,
            model_id=modelId,
            price=price,
            year=form.year.data,
            color=form.color.data,
            description=form.description.data,
            pictures=picture_folder,
            mileage=form.mileage.data,
            fuel_type=form.fuel_type.data,
            gear_type=form.gear_type.data,
        )
        db.session.add(car)
        db.commit()

        vehicle = Vehicles.query.filter_by(Vehicles.make_id == makeId and Vehicles.model_id ==
                                           modId and Vehicles.year == form.year.data and Vehicles.color == form.color.data)
        if form.trade.data:
            trade = Trade(
                user_id=current_user.get_id,
                trade_amount=price,
            )
            db.session.add(trade)
            db.commit()
            return redirect('main.trade_in')

        if form.sell.data:
            return redirect(url_for('main.sell'))

        return redirect(url_for('main.trade_in'))
    return render_template('vehicles/trade_in.html', form=form)


@main.route('/sell', methods=['GET', 'POST'])
def sell():
    form = SellDetailsForm()

    if form.validate_on_submit():
        flash('Your payment has been processed', 'success')
        return redirect(url_for('main.trade_in'))

    return render_template('vehicles/sell_car.html', form=form)


@main.route('/overview/<id>', methods=['GET', 'POST'])
def overview(id):
    vehicle_to_render = Vehicles.query.get(id)
    makes_for_render = Make.query.order_by(Make.make_id.asc())
    models_for_render = Model.query.order_by(Model.model_id.asc())
    trading = Trade.query.order_by(Trade.trade_id.asc())
    return render_template('product_cart.html', car=vehicle_to_render, makes=makes_for_render, models=models_for_render, trade=trading)


@main.route('/checkout/<id>', methods=['GET', 'POST'])
def checkout(id):
    form = CheckoutDetailsForm()
    vehicle_to_render = Vehicles.query.get(id)
    makes_for_render = Make.query.order_by(Make.make_id.asc())
    models_for_render = Model.query.order_by(Model.model_id.asc())
    trading = Trade.query.order_by(Trade.trade_id.asc())

    if form.validate_on_submit():
        flash('Your purchase was successful', 'success')
        return redirect(url_for('main.index'))

    return render_template('checkout.html', form=form, car=vehicle_to_render, makes=makes_for_render, models=models_for_render, trade=trading)
