# Blogging Platform API

A robust and feature-rich RESTful API for managing a blogging platform, built with Django and Django REST Framework.

## Features

- **User Management**
  - User registration and authentication
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
- Nginx (for production deployment)
- Docker and Docker Compose

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/blogging_platform_api.git
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

## Deployment

The project includes Docker configuration for easy deployment:

1. Build and start the containers:
   ```bash
   docker-compose -f deployment.yml up --build
   ```

2. The application will be available at:
   - API: http://localhost/api/
   - Admin interface: http://localhost/admin/

## API Documentation

Detailed API documentation is available at `/api/docs/` when the server is running.

Key endpoints:

- `/api/users/` - User management
- `/api/posts/` - Blog posts
- `/api/comments/` - Comments
- `/api/categories/` - Categories
- `/api/tags/` - Tags

## Testing

Run the test suite:

```bash
python manage.py test
```

For coverage report:

```bash
coverage run manage.py test
coverage report
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
