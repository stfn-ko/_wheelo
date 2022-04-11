from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.main.forms import ContactForm, FAQForm, DeleteQuestionForm, \
    EditQuestionForm, PostForm, EditPostForm, TradeInForm, SellDetailsForm, \
    CheckoutDetailsForm, InsuranceForm, ReviewForm
from app.models import User, FAQ, Post, Vehicles, Model, Make, Trade, Insurance, CarReview, History
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
            picture = save_picture(form.picture.data, 'static/post_pics')
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
                post.picture = save_picture(
                    form.picture.data, 'static/post_pics')
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
    history_for_render = History.query.order_by(History.history_id.asc())
    return render_template('vehicles/car_page.html', car=vehicle_to_render, makes=makes_for_render, models=models_for_render, history=history_for_render)


@main.route('/trade-in', methods=['GET', 'POST'])
@login_required
def trade_in():
    form = TradeInForm()
    #form.make.choices = Make.query.order_by(Make.make_id.asc())
    #form.model.choices = Model.query.order_by(Model.model_id.asc())
    if form.validate_on_submit():

        price = 1000  # use valuation to get price?

        make_exist = Make.query.filter(
            Make.make_name == form.make.data).first()
        if not make_exist:
            make_new = Make(
                make_name=form.make.data,
            )
            db.session.add(make_new)
            db.session.commit()

        newMake = Make.query.filter(Make.make_name == form.make.data).first()
        makeId = newMake.make_id

        model_exist = Model.query.filter(
            Model.model_name == form.model.data).first()
        if not model_exist:
            model_new = Model(
                model_name=form.model.data,
                make_id=makeId
            )
            db.session.add(model_new)
            db.session.commit()

        newModel = Model.query.filter(
            Model.model_name == form.model.data).first()
        modId = newModel.model_id

        picture_folder = str(form.model.data + '_' +
                             form.color.data + '_' + str(form.year.data))
        #filename_one = secure_filename(form.picture_one.data)
        #filename_two = secure_filename(form.picture_two.data)
        #filename_three = secure_filename(form.picture_three.data)
        #form.picture_one.data.save('app/static/car_pics/' + filename_one)
        #form.picture_two.data.save('app/static/car_pics/' + filename_two)
        #form.picture_three.data.save('app/static/car_pics/' + filename_three)

        #f = form.picture_one.data
        # f.save(secure_filename(f.filename))

        if form.picture_one.data:
            image_file_one = save_picture(
                form.picture_one.data, 'static/car_pics')

        if form.picture_two.data:
            image_file_two = save_picture(
                form.picture_two.data, 'static/car_pics')

        if form.picture_three.data:
            image_file_three = save_picture(
                form.picture.data, 'static/car_pics')

        car = Vehicles(
            make_id=int(makeId),
            model_id=int(modId),
            price=int(price),
            year=int(form.year.data),
            color=str(form.color.data),
            description=str(form.description.data),
            pictures=str(picture_folder),
            mileage=int(form.mileage.data),
            fuel_type=str(form.fuel_type.data),
            gear_type=str(form.gear_type.data),
            popular=str("false"),
        )
        db.session.add(car)
        db.session.commit()

        if form.trade.data:
            trade = Trade(
                user_id=int(current_user.get_id()),
                trade_amount=int(price),
            )
            db.session.add(trade)
            db.session.commit()
            flash('You have successfuly selected to trade in your vehicle, your trade will automatically be applied to your purchase', 'success')
            return redirect(url_for('main.trade_in'))

        if form.sell.data:
            flash('You have successfuly selected to sell your vehicle. The amount we will offer you is: ' + price, 'success')
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
    return render_template('order_overview.html', car=vehicle_to_render, makes=makes_for_render, models=models_for_render, trading=trading)


@main.route('/checkout/<id>', methods=['GET', 'POST'])
def checkout(id):
    form = CheckoutDetailsForm()
    vehicle_to_render = Vehicles.query.get(id)
    makes_for_render = Make.query.order_by(Make.make_id.asc())
    models_for_render = Model.query.order_by(Model.model_id.asc())
    trading = Trade.query.order_by(Trade.trade_id.asc())

    if form.validate_on_submit():
        if current_user.get_id():
            trade_delete = Trade.query.filter(Trade.user_id == current_user.get_id()).first()
            db.session.delete(trade_delete)
            
        db.session.delete(vehicle_to_render)
        db.session.commit()
        flash('Your purchase was successful!', 'success')

        return redirect(url_for('main.viewAllCars'))

    return render_template('checkout.html', form=form, car=vehicle_to_render, makes=makes_for_render, models=models_for_render, trading=trading)


@main.route('/car/insurance', methods=['GET', 'POST'])
@login_required
def insurance():
    form = InsuranceForm()
    if form.validate_on_submit():
        img = 'default.jpg'
        if form.insurance_img.data:
            img = save_picture(form.insurance_img.data, 'static/insurace_pics')
        insurance = Insurance(
            fname=form.fname.data,
            lname=form.lname.data,
            bdate=form.bdate.data,
            ref_by=form.ref_by.data,
            property_status=form.property_status.data,
            street_address=form.street_address.data,
            street_address_l2=form.street_address_l2.data,
            city=form.city.data,
            state_prov=form.state_prov.data,
            postal=form.postal.data,
            country=form.country.data,
            email=form.email.data,
            ph_num=form.ph_num.data,
            # br
            hh_ld_amt=form.hh_ld_amt.data,
            hh_info=form.hh_info.data,
            health_insurance=form.health_insurance.data,
            health_insurance_cov=form.health_insurance_cov.data,
            health_insurance_carr=form.health_insurance_carr.data,
            vehicle_info=form.vehicle_info.data,
            vehicle_full_cov=form.vehicle_full_cov.data,
            vehicle_additional=form.vehicle_additional.data,
            additional_info=form.additional_info.data,
            insurance_img=img
        )
        db.session.add(insurance)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('vehicles/car_insurance.html', form=form)


@main.route('/car_reviews/all', methods=['GET', 'POST'])
def allReviews():
    rev = CarReview.query.order_by(CarReview.id.asc())
    return render_template('vehicles/all_car_reviews.html', rev=rev)


@main.route('/car_reviews/<id>', methods=['GET', 'POST'])
def review(id):
    rev = CarReview.query.get_or_404(id)
    return render_template('vehicles/car_review_page.html', rev=rev)


@main.route('/car_reviews/add', methods=['GET', 'POST'])
def addReview():
    form = ReviewForm()
    if form.validate_on_submit():
        img = 'default.jpg'
        if form.image.data:
            img = save_picture(form.image.data, 'static/car_review_pics')
        r = CarReview(
            id=form.id.data,
            title=form.title.data,
            caption=form.caption.data,
            image=img,
            category=form.category.data,
            preview_text=form.preview_text.data
        )
        db.session.add(r)
        db.session.commit()
        return redirect(url_for('main.allReviews'))
    return render_template('vehicles/add_review.html', form=form)


@main.route('/car_reviews/categorized', methods=['GET', 'POST'])
def catReviews():
    ctrev = None
    rev = CarReview.query.order_by(CarReview.id.asc())
    target_string = request.form['category']

    if request.method == 'POST':
        ctrev = CarReview.query.filter(
            or_(
                CarReview.category.contains(target_string),
                CarReview.title.contains(target_string)
            )).all()

    if target_string == 'any':
        return redirect(url_for('main.allReviews'))
    else:
        search_msg = f'{len(ctrev)} review(s) found'

    return render_template('vehicles/categorized_car_reviews.html', ctrev=ctrev, rev=rev, smg=search_msg)


@main.route('/cars/all', methods=['GET', 'POST'])
def viewAllCars():
    cars = Vehicles.query.order_by(Vehicles.id.asc())
    make = Make.query.order_by(Make.make_id.asc())
    model = Model.query.order_by(Model.model_id.asc())
    return render_template('vehicles/all_cars.html', cars=cars, make=make, model=model)


@main.route('/cars/search', methods=['GET', 'POST'])
def viewSearchedCars():
    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    result = Vehicles.query.order_by(Vehicles.id.asc())
    fmodel = Model.query.order_by(Model.model_id.asc())
    fmake = Make.query.order_by(Make.make_id.asc())

    t_make = request.form['make']
    t_model = request.form['model']
    t_color = request.form['color']
    t_registration_1 = request.form['registration_1']
    t_registration_2 = request.form['registration_2']
    t_price_1 = request.form['price_1']
    t_price_2 = request.form['price_2']
    t_mileage_1 = request.form['mileage_1']
    t_mileage_2 = request.form['mileage_2']

    if t_price_1 == '':
        t_price_1 = 0
    if t_registration_1 == '':
        t_registration_1 = 0
    if t_mileage_1 == '':
        t_mileage_1 = 0

    if t_price_2 == '':
        t_price_2 = 9999999999
    elif int(t_price_2) > 9999999999:
        t_price_2 = 9999999999
    if t_registration_2 == '':
        t_registration_2 = 9999999999
    elif int(t_registration_2) > 9999999999:
        t_registration_2 = 9999999999
    if t_mileage_2 == '':
        t_mileage_2 = 9999999999
    elif t_mileage_2 > 9999999999:
        t_mileage_2 = 9999999999

    make_filter = Make.query.filter_by(make_name=t_make).first()
    model_filter = Model.query.filter_by(
        model_name=t_model.capitalize()).first()
    color_filter = Vehicles.query.filter_by(color=t_color.lower()).all()
    registration_filter = intersection(Vehicles.query.filter(Vehicles.year > t_registration_1).all(),
                                       Vehicles.query.filter(Vehicles.year < t_registration_2).all())
    price_filter = intersection(Vehicles.query.filter(Vehicles.price > t_price_1).all(),
                                Vehicles.query.filter(Vehicles.price < t_price_2).all())
    mileage_filter = intersection(Vehicles.query.filter(Vehicles.mileage > t_mileage_1).all(),
                                  Vehicles.query.filter(Vehicles.mileage < t_mileage_2).all())
    if int(t_price_1) < int(t_price_2):
        if int(t_registration_1) < int(t_registration_2):
            if int(t_mileage_1) < int(t_mileage_2):

                if t_make != 'any':
                    result = Vehicles.query.filter_by(
                        make_id=make_filter.make_id).all()
                    if t_model != '' and model_filter is not None:
                        result = Vehicles.query.filter_by(
                            model_id=model_filter.model_id, make_id=make_filter.make_id)

                if t_color != '' and color_filter is not None:
                    result = intersection(color_filter, result)

                if price_filter is not None:
                    result = intersection(price_filter, result)

                if registration_filter is not None:
                    result = intersection(registration_filter, result)

                if mileage_filter is not None:
                    result = intersection(mileage_filter, result)

    return render_template('vehicles/searched_cars.html', result=result, model=fmodel, make=fmake)


@main.route('/history')
def history():
    return render_template('vehicles/history.html')
