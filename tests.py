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


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
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

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Test to show all users page"""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_redirect_to_users(self):
        """Test redirect to /users"""
        with self.client as client:
            resp = client.get('/', follow_redirects = True)
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_display_new_user_form(self):
        """Test new user form page"""
        with self.client as client:
            resp = client.get('users/new')
            html = resp.get_data(as_text = True)

            self.assertIn('new_user', html)

    def test_delete_user(self):
        """Test delete user redirect"""
        with self.client as client:

            resp = client.post(f'/users/{self.user_id}/delete',
                              follow_redirects = True)
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)



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

        self.user_id = test_user.id
        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_posts(self):
        """Test to show all posts on user page"""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            self.assertIn("testing_title", html)

    def test_display_new_post_form(self):
        """Test new user form page"""
        with self.client as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text = True)


            self.assertIn("Add Post for test_first test_last", html)

    def test_make_post(self):
        """Test making a post"""

        with self.client as client:

            resp = client.post(f'/users/{self.user_id}/posts/new',
                                data = {"title": 'unittest_title',
                                    "content": 'unittest_content'},
                                    follow_redirects = True)
            html = resp.get_data(as_text = True)


            self.assertEqual(resp.status_code, 200)
            self.assertIn("unittest_title", html)
