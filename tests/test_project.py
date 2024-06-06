
import pytest
import corkboard
from corkboard import create_app, db, bcrypt
from corkboard.forms import LoginForm
from corkboard.models import User, Board, Comment, Starred
from corkboard.routes import post
from flask_login import current_user
from flask import url_for
from unittest.mock import MagicMock
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
    app.config['SECRET_KEY'] = 'test_secret_key'
    with app.app_context():
        db.create_all()
        hashed_password = bcrypt.generate_password_hash('test_password').decode('utf-8')
        test_user = User(username='test_user', email='test@example.com', password=hashed_password)
        db.session.add(test_user)
        db.session.commit()  # Commit test_user to the database to get its id
        real_post = Board(id=1, title="Test Post", content="This is a test post.", user_id=test_user.id)
        db.session.add(real_post)
        test_comment = Comment(id=1, text="Test Comment", author_id=test_user.id, post_id=real_post.id)
        db.session.add(test_comment)
        test_starred = Starred(id=1, author=test_user.id, post_id=real_post.id)
        db.session.add(test_starred)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()
    




@pytest.fixture
def client(app):
    return app.test_client()


def login(client):
        form = LoginForm()
        form.email.data = 'test@example.com'
        form.password.data = 'test_password'
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            client.post('/login', data=dict(email=form.email.data, password=form.password.data), follow_redirects=True)
        else:
            print("Login failed: Invalid username or password")

def test_login(client):
    response = client.post('/login', data=dict(email='test@example.com', password='test_password'), follow_redirects=True)
    assert response.status_code == 200



# Successful login with correct email and password
def test_successful_login(mocker, client):
    mocker.patch('corkboard.routes.current_user', return_value=mocker.Mock(is_authenticated=False))
    db_session = UnifiedAlchemyMagicMock()
    db_session.add = MagicMock()
    db_session.commit = MagicMock()
    mocker.patch('corkboard.routes.db.session', return_value=db_session)
    mocker.patch('corkboard.routes.flash')
    mocker.patch('corkboard.routes.redirect', return_value='redirected')
    mocker.patch('corkboard.routes.url_for', return_value='/home')
    form_data = {
        'username': 'newuser',
        'password': 'password123'
    }

    response = client.post('/login', data=form_data)
    assert response.status_code == 200

  


# Ensure client fixture returns a test client instance
def test_client_returns_test_client_instance(client):
        assert client is not None
        assert hasattr(client, 'get')
        assert hasattr(client, 'post')
       


# Ensure the function returns a 200 HTTP status code
def test_index_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200


    # Verify that the home function returns the correct template 'home.html'
def test_home_returns_correct_template(client):
        response = client.get('/home')
        assert response.status_code == 200


    # Verify that the function returns the correct template 'starredBoards.html'
def test_returns_correct_template(client):
        login(client)
        response = client.get('/home/favoriteboards')
        assert response.status_code == 200


    # renders the 'landingPage.html' template successfully
def test_renders_landing_page_template_successfully( client):
        response = client.get('/home/landingPage')
        assert response.status_code == 200
      
    # renders the 'about.html' template successfully
def test_renders_about_template_successfully(client):
        response = client.get('/about')
        assert response.status_code == 200
     

 # Successful registration with valid username, email, and password
def test_successful_registration(mocker, client):
    mocker.patch('corkboard.routes.current_user', return_value=mocker.Mock(is_authenticated=False))
    # Create a mock session
    db_session = UnifiedAlchemyMagicMock()
    # Mock the add and commit methods
    db_session.add = MagicMock()
    db_session.commit = MagicMock()
    mocker.patch('corkboard.routes.db.session', return_value=db_session)
    mocker.patch('corkboard.routes.flash')
    mocker.patch('corkboard.routes.redirect', return_value='redirected')
    mocker.patch('corkboard.routes.url_for', return_value='/login')
    form_data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }

    response = client.post('/register', data=form_data)
    assert response.status_code == 200


# User is successfully logged out when already logged in
def test_user_logged_out_when_logged_in(client):
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
     


# renders the contactus.html template successfully
def test_renders_contactus_template_successfully( client):
        response = client.get('/contactus')
        assert response.status_code == 200
        




# Successfully creates a new post with valid title, content, and file
def test_new_post(mocker, client):
    login(client)
    mocker.patch('corkboard.routes.login_required', return_value=True)
    mocker.patch('corkboard.routes.current_user', return_value=mocker.Mock(is_authenticated=True))
    # Create a mock form
    form = MagicMock()
    form.validate_on_submit.return_value = True
    form.title.data = 'Test Title'
    form.content.data = 'Test Content'
    form.file.data = None
    mocker.patch('corkboard.routes.PostForm', return_value=form)
    # Create a mock session
    db_session = UnifiedAlchemyMagicMock()
    # Mock the add and commit methods
    db_session.add = MagicMock()
    db_session.commit = MagicMock()
    mocker.patch('corkboard.routes.db.session', return_value=db_session)
    mocker.patch('corkboard.routes.flash')
    mocker.patch('corkboard.routes.redirect', return_value='redirected')
    mocker.patch('corkboard.routes.url_for', return_value='/home')
    mocker.patch('corkboard.routes.render_template', return_value='rendered')
   

    response = client.post('/post/new', data={'title': 'Test Title', 'content': 'Test Content'})

    assert response.status_code == 200
    
# Successfully retrieves a post by valid post_id
def test_post_route(client):
    post_id = 1  # The id of the post you want to test
    response = client.get(f"/post/{post_id}")
    assert response.status_code == 200
  




def test_update_post(client):
    # Arrange
    login(client)
    post_id = 1  # The id of the post you want to test
    new_title = "Updated Test Post"
    new_content = "This is an updated test post."
    form_data = {
        'title': new_title,
        'content': new_content
    }
    # Act
    response = client.post(f"/post/{post_id}/update", data=form_data, follow_redirects=True)
    # Assert
    assert response.status_code == 200
    
   


def test_user_posts(client):
    # Arrange
    username = 'test_user' 
    expected_post_title = 'Test Post'
    expected_post_content = 'This is a test post.'
    # Act
    response = client.get(f"/user/{username}")
    data = response.get_data(as_text=True)
    # Assert
    assert response.status_code == 200
    assert expected_post_title in data
    assert expected_post_content in data


def test_delete_post_by_author(client, app):
    # Log in as the test user
    login(client)

    # Try to delete the post as the author
    response = client.post('/post/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Your post and associated comments have been deleted!' in response.data

    # Check that the post has been deleted
    with app.app_context():
        post = Board.query.get(1)
        assert post is None

        # Check that the comment and starred post associated with the post have been deleted
        comment = Comment.query.get(1)
        assert comment is None

        starred = Starred.query.get(1)
        assert starred is None

def test_delete_post_by_non_author(client, app):
    # Create another user and try to delete the post as this user
    with app.app_context():
        hashed_password = bcrypt.generate_password_hash('test_password2').decode('utf-8')
        test_user2 = User(username='test_user2', email='test2@example.com', password=hashed_password)
        db.session.add(test_user2)
        db.session.commit()

    # Log in as the second user
    client.post('/login', data=dict(email='test2@example.com', password='test_password2'), follow_redirects=True)

    # Try to delete the post as the second user
    response = client.post('/post/1/delete', follow_redirects=True)
    assert response.status_code == 403


  

def test_like_post(client):
    # Arrange
    login(client)  # Log in as the test user
    post_id = 1  # The id of the post to like

    # Act
    response = client.get(f'/like_post/{post_id}', follow_redirects=True)

    # Assert
    assert response.status_code == 200
    assert b"Post does not exist." not in response.data




def test_search_user(client):
    # Log in the client
    login(client)

    # Test when user exists
    response = client.post('/home/search_user', data=dict(username='test_user'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Post' in response.data  # Assuming 'Test Post' is a post by the test_user

    # Test when user does not exist
    response = client.post('/home/search_user', data=dict(username='nonexistent_user'), follow_redirects=True)
    assert response.status_code == 200
    assert b'User not found.' in response.data



# Successfully creating a comment with valid text and post ID
def test_create_comment_success(mocker, client):
       # Fetch the existing user
        test_user = User.query.filter_by(email='test@example.com').first()
        # Mock current_user
        mocker.patch('flask_login.utils._get_user', return_value=test_user)

        # Create a post to comment on
        post = Board.query.filter_by(title='Test Post').first()
     
        # Send POST request to create comment
        response = client.post(f'/create_comment/{post.id}', data={'text': 'Test Comment'}, follow_redirects=True)
        # Check if the comment was created
        comment = Comment.query.filter_by(text='Test Comment').first()
        assert comment is not None
        assert comment.text == 'Test Comment'
        assert comment.post_id == post.id

        # Check if the response is a redirect to the post page
        assert response.status_code == 200
        assert b'Test Post' in response.data 
  

def test_delete_comment(client):
    # Login first
    login(client)
    # Get the comment to be deleted
    comment = Comment.query.filter_by(id=1).first()
    # Ensure the comment exists before the delete request
    assert comment is not None
    # Send a delete request
    response = client.get(f'/delete_comment/{comment.id}', follow_redirects=True)
    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    # Check that the comment has been deleted
    deleted_comment = Comment.query.filter_by(id=1).first()
    assert deleted_comment is None
