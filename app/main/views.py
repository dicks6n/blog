from flask import render_template, request, redirect, url_for, abort
from . import main
from .forms import BlogForm,CommentForm, UpdateProfile
from ..models import Comment, User, Blog,Member
from .. import db, photos
from ..request import get_quote
from flask_login import login_required, current_user
import markdown2
from ..email import mail_message

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'GraphersBlog'
    quote = get_quote()
    comments = Comment.query.all()
    allBlogs = Blog.query.all()
    del_blog = request.args.get('delete_this')
    del_comment = request.args.get('delete_comment')
    if del_blog:
        Blog.delete_blog(b_id=del_blog)
        return redirect(url_for('main.index'))
    elif del_comment:
        Comment.delete_comment(c_id=del_comment)
        return redirect(url_for('main.index'))
    else:
        return render_template('index.html', title = title, blogs = allBlogs, quote = quote, comments = comments)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    blogs = Blog.query.filter_by(user_id = user_id).order_by(Blog.posted.desc())

    if user is None :
        abort(404)

    return render_template("profilr/profile.html" user = user ,blogs =blogs) 

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    blogs = Blog.query.filter_by(user_id = user.id).order_by(Blog.posted.desc())

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, blogs = blogs) 

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form,user=user)  

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
@main.route('/user/<uname>/blog',methods= ['GET','POST'])
@login_required
def new_blog(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = BlogForm()
    blog = Blog()