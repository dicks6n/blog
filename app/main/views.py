from flask import render_template, request, redirect, url_for, abort
from . import main
from .forms import BlogForm,CommentForm, UpdateProfile

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'GraphersBlog'