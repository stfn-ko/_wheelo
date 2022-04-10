from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, BooleanField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms import TextAreaField, FileField, DecimalField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=5, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contactNumber = StringField('Contact Number', validators=[
                                DataRequired(), Length(min=11, max=11)])
    message = TextAreaField('Message', validators=[
                            DataRequired(), Length(min=2, max=500)])
    submit = SubmitField('Send Message')


class FAQForm(FlaskForm):
    question = TextAreaField(
        'Question', validators=[DataRequired(), Length(min=10, max=400)])
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=3, max=30)])
    submit = SubmitField('Ask')


class EditQuestionForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=3, max=30)])
    question = TextAreaField(
        'Question', validators=[DataRequired(), Length(min=1, max=400)])
    answer = TextAreaField(
        'Answer', validators=[DataRequired(), Length(min=1, max=400)])
    update = SubmitField('Update')
    cancel = SubmitField('Cancel')


class DeleteQuestionForm(FlaskForm):
    delete = SubmitField('Delete')
    cancel = SubmitField('Cancel')


class PostForm(FlaskForm):
    title = StringField('Post Title:', validators=[
                        DataRequired(), Length(min=1, max=50)])
    picture = FileField('Add image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only with extension .jpg or .png')]
    )
    caption = TextAreaField(
        'Text', validators=[DataRequired(), Length(min=1, max=6000)])
    submit = SubmitField('Share')
    cancel = SubmitField('Cancel')


class EditPostForm(FlaskForm):
    title = StringField('Name', validators=[
        DataRequired(), Length(min=5, max=50)])
    caption = TextAreaField(
        'Text', validators=[DataRequired(), Length(min=1, max=6000)])
    picture = FileField('Update image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only with extension .jpg or .png')]
    )
    update = SubmitField('Update')
    delete = SubmitField('Delete')
    cancel = SubmitField('Cancel')


class TradeInForm(FlaskForm):
    #make = SelectField('make', choices=[])
    #model = SelectField('model', choices=[])
    make = StringField('make', validators=[
                       DataRequired(), Length(min=3, max=100)])
    model = StringField('model', validators=[DataRequired(), Length(max=100)])
    color = StringField('color', validators=[
        DataRequired(), Length(min=3, max=20)])
    year = IntegerField('year made', validators=[DataRequired()])
    description = StringField('Description')
    picture_one = FileField('Picture One')
    picture_two = FileField('Picture Two')
    picture_three = FileField('Picture Three')
    mileage = IntegerField('total mileage', validators=[DataRequired()])
    fuel_type = SelectField('fuel type', choices=[('petrol'), ('diesel')])
    gear_type = SelectField('gear type', choices=[('manual'), ('automatic')])
    reg = StringField('car registration number')
    trade = SubmitField('Trade-In')
    sell = SubmitField('Sell')


class SellDetailsForm(FlaskForm):
    name = StringField('Name on the card', validators=[DataRequired()])
    sortCode = IntegerField('Sort Code', validators=[DataRequired()])
    accountNum = IntegerField('Account Number', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address_one = StringField('Address Line One', validators=[DataRequired()])
    address_two = StringField('Address Line Two')
    city = StringField('City', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CheckoutDetailsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address_one = StringField('Address Line One', validators=[DataRequired()])
    address_two = StringField('Address Line Two')
    city = StringField('City', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired()])
    cardNum = IntegerField('Card Number', validators=[DataRequired()])
    expDate = DateField('Expiry Date', format='%d/%m/%Y')
    csv = IntegerField('CSV number', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReviewForm(FlaskForm):
    id = IntegerField('id')
    category = StringField('category')
    title = StringField('title')
    preview_text = StringField('prev text')
    caption = TextAreaField('caption')
    image = FileField('Add image', validators=[FileAllowed(
        ['jpg', 'png'], 'Images only with extension .jpg or .png')])
    submit = SubmitField('Submit')


class InsuranceForm(FlaskForm):
    fname = StringField('First Name*', validators=[DataRequired()])
    lname = StringField('Last Name*', validators=[DataRequired()])
    bdate = DateField('Date of Birth*', format='%Y-%m-%d',
                      validators=[DataRequired()])
    ref_by = StringField('Who were you referred by?')
    property_status = StringField(
        'Do you own the home you live in or do you rent?*', validators=[DataRequired()])
    street_address = StringField(
        'Street Address*', validators=[DataRequired()])
    street_address_l2 = StringField('Street Address Line Two')
    city = StringField('City*', validators=[DataRequired()])
    state_prov = StringField('State/Province*', validators=[DataRequired()])
    postal = StringField('Zip Code/Postal*', validators=[DataRequired()])
    country = StringField('Country*', validators=[DataRequired()])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    ph_num = IntegerField('Phone Number*', validators=[DataRequired()])
    # br
    hh_ld_amt = IntegerField('How many licensed drivers in the home?*')
    hh_info = TextAreaField(
        'Please list all occupants names and date of births')
    health_insurance = BooleanField(
        'Do you have health insurance?(check if true)')
    health_insurance_cov = BooleanField(
        'Is everyone in your home covered under the same health insurance?(check if true)')
    health_insurance_carr = StringField(
        'Who is your health insurance carrier?*', validators=[DataRequired()])
    vehicle_info = StringField(
        'Vehicle Info: Year, Make, Model (optional: Vin #)*', validators=[DataRequired()])
    vehicle_full_cov = BooleanField(
        'Do you want full coverage on your Vehicle?(check if true)')
    vehicle_additional = TextAreaField(
        'If you have more then 1 vehicle then please list them here')
    additional_info = TextAreaField(
        'Anything else you would want the agent to know regarding the auto insurance?')
    insurance_img = FileField('Add image', validators=[FileAllowed(
        ['jpg', 'png'], 'Images only with extension .jpg or .png')])
    submit = SubmitField('Submit')
