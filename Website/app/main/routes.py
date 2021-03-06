from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.main.forms import ContactForm, FAQForm, DeleteQuestionForm, \
    EditQuestionForm, PostForm, DeletePostForm, EditPostForm
from app.models import User, FAQ, Post
from app import db

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():
    posts_for_render = Post.query.order_by(Post.created_at.asc())
    return render_template('index.html', posts=posts_for_render, title='Home')


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


@main.route('/blog/new_post', methods=['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()
    if form.submit.data and form.validate_on_submit():
        p = Post(
            caption=form.caption.data,
            user_id=current_user.get_id()
        )
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('main.index'))
    if form.cancel.data:
        return redirect(url_for('main.index'))
    return render_template('blog/new_post.html', title='New Post', form=form)


@main.route('/blog/delete_post/<id>', methods=['GET', 'POST'])
@login_required
def delPost(id):
    post = Post.query.get_or_404(id)
    form = DeletePostForm()
    if request.method == 'POST' and form.delete.data:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    if form.cancel.data:
        return redirect(url_for('main.index'))
    return render_template('blog/delete_post.html', post=post, title="Delete Post", form=form)


@main.route('/blog/edit_post/<id>', methods=['GET', 'POST'])
@login_required
def editPost(id):
    post = Post.query.get_or_404(id)
    form = EditPostForm()
    if request.method == 'GET':
        form.caption.data = post.caption
    elif request.method == 'POST':
        if form.update.data and form.validate_on_submit():
            post.caption = request.form['caption']
            db.session.commit()
            return(redirect(url_for('main.index')))
        if form.cancel.data:
            return(redirect(url_for('main.index')))
    return render_template('blog/edit_post.html',  post=post, title='Edit Post', form=form)