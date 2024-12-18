# Blogging Platform API

A modern RESTful API for a blogging platform built with Django REST Framework. This API allows users to create, read, update, and delete blog posts, manage categories, and interact through comments.

## Features

### Core Features
- User authentication and authorization using JWT
- Blog post management (CRUD operations)
- Category and tag organization
- Commenting system
- User profiles

### Technical Features
- Token-based authentication (JWT)
- RESTful API design
- Swagger/OpenAPI documentation
- Modular project structure
- Admin interface

## Tech Stack

- Python 3.8+
- Django 4.2.17
- Django REST Framework 3.15.2
- djangorestframework-simplejwt 5.3.0
- django-cors-headers 4.3.0
- drf-yasg 1.21.7 (API Documentation)

## Project Structure
blogging_platform_api/ ├── apps/ │ ├── users/ # User authentication and profiles │ ├── posts/ # Blog posts and tags │ ├── categories/ # Post categories │ └── comments/ # Post comments ├── core/ # Project settings └── requirements.txt # Project dependencies

Code
CopyInsert

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Users
- `POST /api/users/` - Register new user
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/` - Update user profile

### Posts
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create new post
- `GET /api/posts/{id}/` - Get post details
- `PUT /api/posts/{id}/` - Update post
- `DELETE /api/posts/{id}/` - Delete post

### Categories
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create new category
- `GET /api/categories/{id}/` - Get category details

### Comments
- `POST /api/posts/{id}/comments/` - Add comment to post
- `GET /api/posts/{id}/comments/` - Get post comments

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yazzy01/blogging_platform_api.git
cd blogging_platform_api
