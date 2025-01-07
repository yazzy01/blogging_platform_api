# Blogging Platform API

A robust and feature-rich RESTful API for managing a blogging platform, built with Django and Django REST Framework.

## Project Status
🚀 **BE Capstone Project - In Progress**
- Start Date: December 16, 2024
- Expected Completion: January 10, 2025
- Current Status: API Development and Documentation Phase

## Features

- **User Management**
  - User registration and authentication (JWT-based)
  - Profile management with avatar support
  - Email verification
  - Password reset functionality
  - Activity tracking and security features

- **Posts Management**
  - CRUD operations for blog posts
  - Rich text content with image support
  - Categories and tags
  - Post likes and view counting
  - Related posts suggestions

- **Comments System**
  - Nested comments (one level deep)
  - Comment likes
  - Comment moderation
  - Real-time notifications

- **Categories and Tags**
  - Hierarchical categories (one level deep)
  - Tag management
  - Post filtering by categories and tags

## Tech Stack

- Python 3.9+
- Django 4.2+
- Django REST Framework
- PostgreSQL
- Redis (for caching and async tasks)
- Swagger/OpenAPI (for API documentation)
- JWT Authentication

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token
- `POST /api/auth/password-reset/` - Request password reset

### Users
- `GET /api/users/` - List users
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user profile
- `GET /api/users/me/` - Get current user profile

### Posts
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create new post
- `GET /api/posts/{id}/` - Get post details
- `PUT /api/posts/{id}/` - Update post
- `DELETE /api/posts/{id}/` - Delete post
- `POST /api/posts/{id}/like/` - Like/unlike post

### Comments
- `GET /api/posts/{id}/comments/` - List post comments
- `POST /api/posts/{id}/comments/` - Add comment
- `PUT /api/comments/{id}/` - Update comment
- `DELETE /api/comments/{id}/` - Delete comment

### Categories & Tags
- `GET /api/categories/` - List categories
- `GET /api/tags/` - List tags
- `POST /api/categories/` - Create category
- `POST /api/tags/` - Create tag

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yazzy01/blogging_platform_api.git
   cd blogging_platform_api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

- Interactive API documentation is available at `/api/swagger/` when the server is running
- OpenAPI schema available at `/api/schema/`

## Testing

Run the test suite:
```bash
python manage.py test
```

## Contributing

This project is part of a BE Capstone Project and is currently under active development.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Yassir Rzigui
- GitHub: [@yazzy01](https://github.com/yazzy01)
- Email: rziguiyassir@gmail.com
