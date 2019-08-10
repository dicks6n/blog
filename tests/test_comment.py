import unittest
from app.models import Comment, User
from app import db

class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.user_James = User(username = 'James',password = 'potato', email = 'james@ms.com')
        self.new_comment = Comment(blog_id=12345,title='comment for pitches',comment='This pitch is the best thing since sliced bread',user = self.user_James)


    def tearDown(self):
        Comment.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.blog_id,12345)
        self.assertEquals(self.new_comment.title,'comment for pitches')
        self.assertEquals(self.new_comment.comment,'This pitch is the best thing since sliced bread')
        self.assertEquals(self.new_comment.user,self.user_James)

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)

    def test_get_comment_by_id(self):
        self.new_comment.save_comment()
        got_comments = comment.get_comments(12345)
        self.assertTrue(len(got_comments) == 1)