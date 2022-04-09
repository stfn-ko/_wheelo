from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, BooleanField, SubmitField
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
