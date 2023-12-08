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



## Authors 

Calkra15@outlook.com

## Acknowledgments

- Credit any resources, libraries, or individuals you'd like to acknowledge.

## Contact

If you have any questions or need support, you can reach me at Calkra15@outlook.com
.


