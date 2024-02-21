# News Blog API using Django Rest Framework

This API provides functionality for managing a news blog platform with user authentication, blog management, comments, likes, and search features.

## Features

### Authentication System

- **Register:** New users can sign up for an account providing necessary details.
- **Login:** Existing users can log in securely.
- **Forgot Password:** Option for users to reset their passwords via email.
- **Reset Password:** Users can reset their passwords securely.

### User Permissions

- **User Roles:** User will be author.
- **Authorization:** Users can only create, edit, read, update their own blogs/comments and also leave the comments on other users blogs and also like the comment.

### Blog Management

- **Create Blog:** Users can create new blog posts.
- **Edit Blog:** Ability to modify existing blog posts.
- **Delete Blog:** Users can remove their own blogs.
- **View All Blogs:** Users can see all blog posts.

### Comments and Likes

- **Add Comment:** Users can comment on blog posts.
- **Like Blogs:** Option to like blog posts.

### Search Functionality

- **Search by Content:** Users can search blogs by content.
- **Search by Title:** Searching blogs by title is supported.
- **Search by Category:** Filtering blogs by category.
- **Combined Search:** Option to perform a combined search (content, title, category).

## Endpoints

### Authentication Endpoints

- `/api/accounts/user/`: POST request to create a new user.
- `/api/accounts/login/`: POST request for user login.
- `/api/accounts/logout`: POST request to log out the user.
- `/api/accounts/reset/<uid>/<token>/`: POST request to reset password.
- `/api/accounts/refresh/`: For accessing the Token.


### Blog Endpoints

- `/api/blog/public/`: GET request to retrieve all blogs.
- `/api/blog/public/:id/`: GET request to retrieve a specific blog.
- `/api/blog/public/:id/like/`: GET request to add like.
- `/api/blog/`: POST request to create a new blog.
- `/api/blog/:id/`: PATCH request to edit a specific blog.
- `/api/blog/:id/`: DELETE request to delete a specific blog.
- `/api/blog/`: GET request to retrieve a specific user blog.
- `/api/blogs/:id/comment/`: GET request to retrieve comments for a specific blog.
- `/api/blog/public/:id/comment/`: POST request to add a comment to a specific blog.
- `/api/blog/categories/`: GET request to fetch all the categories.


### Search Endpoints

- `/api/blog/public/?search=search_query`: GET request to search blogs.

## Tech Stack

- **Django:** Backend framework.
- **Django Rest Framework (DRF):** For building RESTful APIs.
- **Database:**  SqlLite.
- **Authentication:** JWT.


# Model Structure

## User Model
The `User` model extends Django's `AbstractUser` class and represents users in the system.

- **Fields:**
  - `email`: Email address of the user. (Unique)
  - `forget_password_token`: Token for resetting the user's password. (Optional)
  - `email_token`: Token for email verification. (Optional)

- **Methods:**
  - `__str__()`: Returns the email address of the user.

## Category Model
The `Category` model represents categories for blogs.

- **Fields:**
  - `name`: Name of the category.
  - `created_at`: Date and time when the category was created.
  - `updated_at`: Date and time when the category was last updated.

- **Methods:**
  - `__str__()`: Returns the name of the category or a default string if the name is empty.

## Blog Model
The `Blog` model represents individual blog posts.

- **Fields:**
  - `category`: Foreign key to the `Category` model representing the category of the blog.
  - `user`: Foreign key to the `User` model representing the owner of the blog.
  - `image`: Image associated with the blog.
  - `title`: Title of the blog.
  - `content`: Content of the blog.
  - `likes`: Many-to-many relationship with users representing users who liked the blog.
  - `created_at`: Date and time when the blog was created.
  - `updated_at`: Date and time when the blog was last updated.

- **Methods:**
  - `__str__()`: Returns the title of the blog or a default string if the title is empty.

## Comment Model
The `Comment` model represents comments on blog posts.

- **Fields:**
  - `user`: Foreign key to the `User` model representing the user who posted the comment.
  - `blog`: Foreign key to the `Blog` model representing the blog the comment belongs to.
  - `content`: Content of the comment.
  - `created_at`: Date and time when the comment was created.
  - `updated_at`: Date and time when the comment was last updated.

- **Methods:**
  - `__str__()`: Returns the content of the comment or a default string if the content is empty.



## Continuous Integration and Testing

- The project follows best practices for continuous integration and testing to ensure code quality and reliability. Key points in this process include:

### Automated Testing


1. **Directory Structure:**
   - Organize your tests within the `tests` directory in your Django app.

### Test Classes

2. **Use Django's `TestCase`:**
   - Utilize Django's `TestCase` class for  test classes.

### Descriptive Naming

3. **Naming Conventions:**
   - Choose descriptive names for your test classes and methods. Follow a naming convention such as `TestAddBlog`.

### Test Fixtures

4. **Fixture Setup:**
   - Create necessary fixtures or use Django's `setUp` method to set up test data.

### Use Appropriate Assertions

5. **Django TestCase Assertions:**
   - When writing tests for  Django application, utilize assertions provided by the Django `TestCase` class. Common assertions include:
     - `assertEqual(a, b)`: Check if `a` and `b` are equal.
     - `assertNotEqual(a, b)`: Check if `a` and `b` are not equal.
     - `assertTrue(x)`: Check if `x` is `True`.
     - `assertFalse(x)`: Check if `x` is `False`.
     - `assertRaises(exception, callable, *args, **kwargs)`: Check if calling `callable(*args, **kwargs)` raises the specified exception.
     - ... and more.

   - Refer to the [Django TestCase documentation](https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.TestCase) for a comprehensive list of assertions available.

   - Example:
     ```python
     from django.test import TestCase

     class YourTestCase(TestCase):
         def test_example(self):
             value = 42
             self.assertEqual(value, 42, "The value should be 42")
           

### Comprehensive Coverage

6. **Cover Critical Paths:**
   - Aim for comprehensive test coverage, ensuring that critical code paths are tested thoroughly.

### Isolation

7. **Test Isolation:**
   - Ensure each test is isolated and does not depend on the state left behind by other tests.

## Running Tests

To run tests for the blog institute Django application, execute the following command:

```bash
python manage.py test accounts
python manage.py test blog



## DEPLOYMENT

This section provides step-by-step instructions on how to deploy the Blogs Institute Django application on Heroku. 

### Prerequisites

Before you begin, make sure you have the following:

- A [Heroku account](https://signup.heroku.com/) .
- [Git](https://git-scm.com/) installed on your local machine.
- The [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed.

### Deployment Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/caleb1711/news-blog-api.git
   cd news-blog-api

   heroku create news-blog-api

   heroku config:set SECRET_KEY='your_secret_key'
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=*
   heroku config:set EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   heroku config:set EMAIL_HOST=smtp.gmail.com
   heroku config:set EMAIL_PORT=port
   heroku config:set EMAIL_USE_TLS=True
   heroku config:set EMAIL_USE_SSL=False 
   heroku config:set EMAIL_HOST_USER=hostemsail  
   heroku config:set EMAIL_HOST_PASSWORD=password
   heroku config:set DEFAULT_FROM_EMAIL=Blog Institute <email>

   git push heroku main

   heroku run python manage.py migrate

   heroku run python manage.py createsuperuser

   heroku open

- Make sure to set the ALLOWED_HOSTS environment variable on Heroku to the domain name of your app.
- I also enable the the automatic deployments with main branch.

## Setup and Installation

1. Clone the repository (`https://github.com/caleb1711/news-blog-api`).
2. Install dependencies (`pip install -r requirements.txt`).
3. Configure database settings in `settings.py`.
4. Run migrations (`python manage.py makemigrations` and `python manage.py migrate`).
5. Start the server (`python manage.py runserver`).

## Usage

- Ensure to authenticate users for accessing protected endpoints.
- Use appropriate HTTP methods (GET, POST, PUT, DELETE) for respective actions.

## Contributing

Feel free to contribute by submitting pull requests, reporting issues, or suggesting improvements.



## Authors 

Calkra15@outlook.com

## Acknowledgments

### Frameworks and Libraries
- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Python](https://www.python.org/)

### Tools and Packages
- [Requests](https://docs.python-requests.org/en/latest/) useing this only for testing purpose

### Email Sending
- [SMTP Library](https://docs.python.org/3/library/smtplib.html) 


### Technologies
- Python
- Django
- RESTful API principles



## Contact

If you have any questions or need support, you can reach me at Calkra15@outlook.com
.


