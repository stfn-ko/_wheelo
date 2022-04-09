from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, BooleanField, SubmitField
from wtforms import TextAreaField, FileField, DecimalField, IntegerField, SelectField, DateField
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
    make = StringField('make', validators=[DataRequired(), Length(min=3, max=200)])
    model = StringField('model', validators=[DataRequired(), Length(min=3, max=200)])
    color = StringField('color', validators=[
                       DataRequired(), Length(min=3, max=20)])
    year = IntegerField('year made', validators=[DataRequired(), Length(4)])
    description = StringField('Description')
    picture_one = FileField('Picture One')
    picture_two = FileField('Picture Two')
    picture_three = FileField('Picture Three')
    mileage = IntegerField('total mileage', validators=[DataRequired()])
    fuel_type = SelectField('fuel type', choices=[('petrol'), ('diesel')])
    gear_type = SelectField('gear type', choices=[('manual'), ('automatic')])
    reg = StringField('car registration number', validators=[Length(7)])
    trade = SubmitField('Trade-In')
    sell = SubmitField('Sell')

class SellDetailsForm(FlaskForm):
    name = StringField('Name on the card', validators=[DataRequired()])
    sortCode = IntegerField('Sort Code', validators=[DataRequired(), Length(6)])
    accountNum = IntegerField('Account Number', validators=[DataRequired(), Length(8)])
    submit = SubmitField('Submit')


class CheckoutDetailsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address_one = StringField('Address Line One', validators=[DataRequired()])
    address_two = StringField('Address Line Two')
    city = StringField('City', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired()])
    cardNum = IntegerField('Card Number', validators=[DataRequired()])
    expDate = DateField('Expiry Date', format='%d/%m/%Y', validators=[DataRequired()])
    csv = IntegerField('CSV number', validators=[DataRequired(), Length(3)])
    submit = SubmitField('Submit')