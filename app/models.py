from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Quote:
    '''
    Quote class to hold random quote
    '''

    def __init__(self, author, quote, permalink):
        self.author = author
        self.quote = quote
        self.permalink = permalink

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), index = True)
    email = db.Column(db.String(255), unique = True, index = True)
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String(255))
    blogs = db.relationship("Blog", backref= "user", lazy="dynamic")
    comments = db.relationship("Comment", backref= "user", lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User {self.username}'

class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))


class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key = True)
    blog_pic_path = db.Column(db.String(255))
    title = db.Column(db.String(255))
    message = db.Column(db.String(255))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship("Comment", backref = "blog", lazy = "dynamic")

    def delete_blog(b_id):
        blog = Blog.query.filter_by(id = b_id).first()
        db.session.delete(blog)
        db.session.commit()

    def get_comments(self):
        blog = Blog.query.filter_by(id = self.id).first()
        comments = Comment.query.filter_by(blog_id = blog.id).order_by(Comment.posted.desc())
        return comments

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key = True)
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"))
    title = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(blog_id = id).all()
        return comments

    def delete_comment(c_id):
        comment = Comment.query.filter_by(id = c_id).first()
        db.session.delete(comment)
        db.session.commit()

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255))
    username = db.Column(db.String(255), index = True)