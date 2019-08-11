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
