```markdown
# API Authentication Documentation

This API uses JSON Web Tokens (JWT) for authentication. JWT is a token-based authentication system that allows secure transmission of information between parties as a JSON object.

## Authentication Setup

The API uses `djangorestframework-simplejwt` for JWT implementation. Authentication is configured in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}
```

## Authentication Endpoints

### 1. Obtain Token Pair
- **URL**: `/api/token/`
- **Method**: `POST`
- **Description**: Get access and refresh tokens
- **Request Body**:
  ```json
  {
      "username": "your_username",
      "password": "your_password"
  }
  ```
- **Response**:
  ```json
  {
      "refresh": "your.refresh.token",
      "access": "your.access.token"
  }
  ```

### 2. Refresh Token
- **URL**: `/api/token/refresh/`
- **Method**: `POST`
- **Description**: Get new access token using refresh token
- **Request Body**:
  ```json
  {
      "refresh": "your.refresh.token"
  }
  ```
- **Response**:
  ```json
  {
      "access": "your.new.access.token"
  }
  ```

## How to Test

### Create a user (if you haven't already):
```bash
python manage.py createsuperuser
```

### Get tokens:
```bash
curl -X POST http://0.0.0.0:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
```

### Use the access token to make authenticated requests:
```bash
curl http://0.0.0.0:8000/api/posts/ \
     -H "Authorization: Bearer your.access.token"
```

### When the access token expires, use the refresh token to get a new one:
```bash
curl -X POST http://0.0.0.0:8000/api/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "your.refresh.token"}'
```

## Protected Endpoints

All API endpoints require authentication except:

- `/api/token/` (POST)
- `/api/token/refresh/` (POST)

Protected endpoints include:

- `/api/posts/` (GET, POST)
- `/api/posts/<id>/` (GET, PUT, PATCH, DELETE)
- `/api/categories/` (GET, POST)
- `/api/categories/<id>/` (GET, PUT, PATCH, DELETE)

## Error Responses

### Unauthorized Access (401)
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Invalid Token (401)
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```

## Security Best Practices

- Access tokens have a short lifetime (1 hour)
- Refresh tokens have a longer lifetime (1 day)
- HTTPS should be used in production
- Tokens should be stored securely on the client side
- Sensitive data is never included in tokens
```
