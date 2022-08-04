from unittest import TestCase

from app import app, db
from models import User, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class PostViewTestCase(TestCase):
    """Test views for posts."""

    def setUp(self):
        """Create test client, add sample data."""

        Post.query.delete()
        User.query.delete()
        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url=None,
        )

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        test_post = Post(
            title = 'testing_title',
            content = 'testing_content',
            user_id = test_user.id
        )

        second_post = Post(
            title = 'testing_title_2',
            content = 'testing_content_2',
            user_id = second_user.id
        )

        db.session.add_all([test_post, second_post])
        db.session.commit()

        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_posts(self):
        """Test to show all posts on user page"""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            breakpoint()
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            self.assertIn("testing_title", html)