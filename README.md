# Django REST Framework User Authentication with JWT

A comprehensive Django REST Framework project implementing JWT-based user authentication with role-based access control (Admin and User roles) and complete User CRUD operations using generic views.

## Features

### Authentication System
- **JWT-based Authentication** using `djangorestframework-simplejwt`
- **Role-based Access Control** (Admin and User roles)
- **Custom User Model** with extended fields
- **Secure Password Management** with validation
- **Token Refresh** mechanism
- **User Registration** and **Login/Logout** endpoints

### User Management (CRUD)
- **List Users** with search and filtering
- **Create Users** (Admin only)
- **View User Details** (Users can view their own, Admins can view any)
- **Update User Information** (Users can update their own, Admins can update any)
- **Delete Users** (Admin only)
- **Toggle User Status** (Admin only)
- **User Statistics** (Admin only)

### Role System
- **Admin Role**: Full access to all users and administrative functions
- **User Role**: Limited access to their own profile and data

## Project Structure

```
User_auth/
├── authentication/          # Authentication app
│   ├── models.py           # Custom User model
│   ├── serializers.py      # Authentication serializers
│   ├── views.py            # Authentication views
│   ├── permissions.py      # Custom permissions
│   ├── urls.py             # Authentication URLs
│   └── admin.py            # Admin configuration
├── users/                  # User CRUD app
│   ├── serializers.py      # User CRUD serializers
│   ├── views.py            # User CRUD views (generic views)
│   └── urls.py             # User CRUD URLs
├── user_auth_project/      # Main project
│   ├── settings.py         # Project settings
│   └── urls.py             # Main URL configuration
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|---------|
| POST | `/api/auth/register/` | User registration | Public |
| POST | `/api/auth/login/` | User login | Public |
| POST | `/api/auth/logout/` | User logout | Authenticated |
| POST | `/api/auth/token/refresh/` | Refresh JWT token | Public |
| GET/PUT | `/api/auth/profile/` | User profile | Authenticated |
| PUT | `/api/auth/change-password/` | Change password | Authenticated |
| GET | `/api/auth/user-info/` | Current user info | Authenticated |

### User CRUD Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|---------|
| GET | `/api/users/` | List all users | Authenticated |
| POST | `/api/users/` | Create new user | Admin only |
| GET | `/api/users/{id}/` | Get user details | Owner or Admin |
| PUT/PATCH | `/api/users/{id}/` | Update user | Owner or Admin |
| DELETE | `/api/users/{id}/` | Delete user | Admin only |
| GET | `/api/users/stats/` | User statistics | Admin only |
| POST | `/api/users/{id}/toggle-status/` | Toggle user status | Admin only |

### API Overview
| Method | Endpoint | Description | Access |
|--------|----------|-------------|---------|
| GET | `/api/` | API overview and documentation | Public |

## Installation and Setup

### 1. Clone and Setup
```bash
cd User_auth
pip install -r requirements.txt
```

### 2. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## Usage Examples

### 1. User Registration
```bash
POST /api/auth/register/
Content-Type: application/json

{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "strongpassword123",
    "password_confirm": "strongpassword123",
    "role": "user"
}
```

### 2. User Login
```bash
POST /api/auth/login/
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "strongpassword123"
}
```

Response:
```json
{
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token",
    "user": {
        "id": 1,
        "email": "john@example.com",
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "role": "user",
        "is_admin": false,
        "full_name": "John Doe"
    }
}
```

### 3. List Users (with filtering)
```bash
GET /api/users/?search=john&role=user&is_active=true
Authorization: Bearer {jwt_access_token}
```

### 4. Create User (Admin only)
```bash
POST /api/users/
Authorization: Bearer {admin_jwt_token}
Content-Type: application/json

{
    "username": "newuser",
    "email": "newuser@example.com",
    "first_name": "New",
    "last_name": "User",
    "password": "password123",
    "password_confirm": "password123",
    "role": "user",
    "is_active": true
}
```

### 5. Update User
```bash
PUT /api/users/1/
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
    "first_name": "Updated",
    "last_name": "Name",
    "email": "updated@example.com"
}
```

### 6. Get User Statistics (Admin only)
```bash
GET /api/users/stats/
Authorization: Bearer {admin_jwt_token}
```

Response:
```json
{
    "stats": {
        "total_users": 10,
        "active_users": 8,
        "inactive_users": 2,
        "admin_users": 2,
        "regular_users": 8,
        "recent_registrations": 3
    }
}
```

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer {jwt_access_token}
```

### Token Refresh
When the access token expires, use the refresh token to get a new access token:

```bash
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "jwt_refresh_token"
}
```

## Role-Based Permissions

### Admin Role (`admin`)
- Can perform all CRUD operations on users
- Can view user statistics
- Can toggle user status (activate/deactivate)
- Can create new users
- Can delete users (except themselves)
- Can view any user's profile

### User Role (`user`)
- Can view their own profile
- Can update their own profile
- Can change their own password
- Can view list of users (limited information)
- Cannot create, delete, or manage other users
- Cannot access admin-only endpoints

## Security Features

- **Password Validation**: Strong password requirements
- **JWT Token Security**: Access and refresh token mechanism
- **Role-based Access**: Granular permissions based on user roles
- **Input Validation**: Comprehensive data validation
- **CORS Configuration**: Configured for frontend integration
- **User Status Management**: Ability to activate/deactivate users

## Models

### User Model
```python
class User(AbstractUser):
    role = CharField(choices=['admin', 'user'], default='user')
    email = EmailField(unique=True)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_active = BooleanField(default=True)
```

## Testing

Test the API using tools like:
- **Postman** or **Insomnia** for API testing
- **Django Admin** at `/admin/` for user management
- **API Overview** at `/api/` for endpoint documentation

## Default Admin Account

A default admin user is created with:
- **Username**: admin
- **Email**: admin@example.com
- **Password**: admin123
- **Role**: admin

⚠️ **Change the default password in production!**

## Configuration

### JWT Settings
Located in `settings.py`:
- Access token lifetime: 60 minutes
- Refresh token lifetime: 1 day
- Token rotation enabled

### CORS Settings
Configured for localhost development. Update for production use.

## Production Considerations

1. **Change SECRET_KEY** in settings.py
2. **Update CORS settings** for your domain
3. **Use environment variables** for sensitive data
4. **Configure proper database** (PostgreSQL recommended)
5. **Set DEBUG = False**
6. **Configure static files serving**
7. **Use HTTPS** in production

## Dependencies

- Django 5.2.4
- Django REST Framework 3.15.2
- djangorestframework-simplejwt 5.3.0
- django-cors-headers 4.4.0

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is for educational purposes.
