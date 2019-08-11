import unittest
from app.models import Blog,User,Comment

class TestPitch(unittest.TestCase):
    """
    This is the class which we will use to do tests for the Pitch
    """

    def setUp(self):
        """
        This will create an instance of the User and Pitch before each test case
        """
        self.new_user = User(username = "Adano")
        self.new_blog = Blog(title = "blog", user = self.new_user)

    def tearDown(self):
        """
        Will delete all the info from the db
        """
        Blog.query.delete()
        User.query.delete()
        Comment.query.delete()

    def test_instance(self):
        """
        Will test whether the new_pitch is an instance of Pitch
        """
        self.assertTrue(isinstance(self.new_blog, Blog))

    def test_init(self):
        """
        Will test whether the new_pitch is instantiated correctly
        """

        self.assertEquals(self.new_blog.title, "blog")

    def test_save_blog(self):
        """
        Will test whether the user is saved into the database
        """
        self.new_blog.save_blog()
        blogs = Blog.query.all()
        self.assertTrue(len(blogs) > 0)

    def test_relationship_user(self):
        """
        Will test whether the pitch is correctly related to the user who posted it
        """
        user = self.new_blog.blog.username
        self.assertTrue(user == "Adano")
