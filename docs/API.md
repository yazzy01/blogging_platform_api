# Blog Platform API Documentation

## Authentication Endpoints

### User Registration
- **URL**: `/api/users/register/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Response**: Returns user data and sends verification email

### Social Authentication
- **Google Login**: `/api/users/social/login/google-oauth2/`
- **GitHub Login**: `/api/users/social/login/github/`
- **Callback URLs**:
  - Google: `/api/users/social/callback/google-oauth2/`
  - GitHub: `/api/users/social/callback/github/`

### Account Activation
- **URL**: `/api/users/activate/{uidb64}/{token}/`
- **Method**: `GET`
- **Response**: Activates user account

### Password Reset
- **Request Reset**:
  - URL: `/api/users/password/reset/`
  - Method: `POST`
  - Body: `{"email": "string"}`

- **Confirm Reset**:
  - URL: `/api/users/password/reset/confirm/{uidb64}/{token}/`
  - Method: `POST`
  - Body: `{"new_password": "string"}`

## User Profile Endpoints

### Profile Management
- **Get Profile**:
  - URL: `/api/users/profile/`
  - Method: `GET`
  - Response: Returns user profile data

- **Update Profile**:
  - URL: `/api/users/profile/`
  - Method: `PATCH`
  - Body:
    ```json
    {
      "first_name": "string",
      "last_name": "string",
      "profile": {
        "bio": "string",
        "location": "string",
        "website": "string",
        "birth_date": "date",
        "twitter": "string",
        "github": "string",
        "linkedin": "string"
      }
    }
    ```

## User Activity Endpoints

### Activity Tracking
- **List Activities**:
  - URL: `/api/users/activities/`
  - Method: `GET`
  - Response: Returns list of user activities

- **Activity Statistics**:
  - URL: `/api/users/activities/stats/`
  - Method: `GET`
  - Response: Returns activity statistics and trends

- **Most Active Times**:
  - URL: `/api/users/activities/most-active-times/`
  - Method: `GET`
  - Response: Returns activity patterns by hour and day

## Blog Post Endpoints

### Posts
- **List Posts**:
  - URL: `/api/posts/`
  - Method: `GET`
  - Query Parameters:
    - `status`: Filter by status (draft/published)
    - `category`: Filter by category
    - `author`: Filter by author
    - `search`: Search in title and content

- **Create Post**:
  - URL: `/api/posts/`
  - Method: `POST`
  - Body:
    ```json
    {
      "title": "string",
      "content": "string",
      "status": "string",
      "categories": [int],
      "tags": [string]
    }
    ```

- **Update Post**:
  - URL: `/api/posts/{id}/`
  - Method: `PUT/PATCH`

- **Delete Post**:
  - URL: `/api/posts/{id}/`
  - Method: `DELETE`

## Category Endpoints

### Categories
- **List Categories**:
  - URL: `/api/categories/`
  - Method: `GET`

- **Create Category**:
  - URL: `/api/categories/`
  - Method: `POST`
  - Body:
    ```json
    {
      "name": "string",
      "description": "string"
    }
    ```

## Comment Endpoints

### Comments
- **List Post Comments**:
  - URL: `/api/posts/{post_id}/comments/`
  - Method: `GET`

- **Add Comment**:
  - URL: `/api/posts/{post_id}/comments/`
  - Method: `POST`
  - Body:
    ```json
    {
      "content": "string",
      "parent": int  // Optional, for replies
    }
    ```

## Error Responses

All endpoints may return the following error responses:

- **400 Bad Request**:
  ```json
  {
    "error": "Error description"
  }
  ```

- **401 Unauthorized**:
  ```json
  {
    "detail": "Authentication credentials were not provided."
  }
  ```

- **403 Forbidden**:
  ```json
  {
    "detail": "You do not have permission to perform this action."
  }
  ```

- **404 Not Found**:
  ```json
  {
    "detail": "Not found."
  }
  ```

## Authentication

Most endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Rate Limiting

API requests are rate limited to:
- Authenticated users: 1000 requests per hour
- Anonymous users: 100 requests per hour
