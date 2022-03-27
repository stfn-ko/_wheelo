from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField 
from wtforms import TextAreaField, FileField, DecimalField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange


class ContactForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=5, max=100)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	contactNumber = StringField('Contact Number', validators=[DataRequired(), Length(min=11, max=11)])
	message = TextAreaField('Message', validators=[DataRequired(), Length(min=2, max=500)])
	submit = SubmitField('Send Message')


class FAQForm(FlaskForm):
    question = TextAreaField(
        '', validators=[DataRequired(), Length(min=10, max=400)])
    name = StringField('', validators=[DataRequired(), Length(min=3, max=30)])
    submit = SubmitField('Ask')

class DeleteQuestionForm(FlaskForm):
    delete = SubmitField('Delete')
    cancel = SubmitField('Cancel')
