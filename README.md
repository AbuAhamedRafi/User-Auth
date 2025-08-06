# 🚀 Django REST API - User Authentication & Product Management

A **production-ready** Django REST Framework API featuring JWT authentication, role-based permissions, and comprehensive product management. Built with clean architecture principles and 100% class-based views.

## 📋 Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Permissions](#permissions)
- [Development](#development)

## ✨ Features

### 🔐 Authentication System
- **JWT-based Authentication** with access & refresh tokens
- **Role-based Access Control**: Admin, Moderator, User
- **Custom User Model** with extended fields
- **Secure Registration & Login**
- **Password Management** with validation
- **Token Refresh** mechanism

### 👥 User Management
- **Complete CRUD operations** with role-based access
- **User Statistics** and analytics
- **Account Status Management** (activate/deactivate)
- **Search & Filtering** capabilities
- **Profile Management**

### 📦 Product & Category Management
- **Category Management**: Full CRUD with hierarchical organization
- **Product Management**: Advanced inventory and catalog management
- **Stock Tracking** and availability management
- **Statistics & Analytics** for business insights
- **Advanced Filtering**: By category, price range, stock status
- **Soft Delete** for data integrity

### 🛡️ Security & Permissions
- **Role-based Access Control** with granular permissions
- **JWT Token Security** with blacklisting
- **Input Validation** and sanitization
- **CORS Configuration** for cross-origin requests
- **Password Strength Validation**

## 🏗️ Architecture

### Clean Code Principles
- **100% Class-based Views** using Django REST Framework generics
- **DRY Implementation** with shared utility functions
- **Streamlined Permissions** (6 essential permission classes)
- **Professional Error Handling** with consistent responses
- **Modular App Structure** for maintainability

### Technology Stack
- **Backend**: Django 5.2.4, Django REST Framework 3.15.2
- **Authentication**: JWT with `djangorestframework-simplejwt`
- **Database**: PostgreSQL (configurable)
- **API Documentation**: Built-in browsable API

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL (or SQLite for development)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbuAhamedRafi/User-Auth.git
   cd User-Auth
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   ```bash
   # Copy environment file
   cp .env.example .env
   # Edit .env with your database settings
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

7. **Access the API**
   - API Root: http://127.0.0.1:8000/api/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API Browser: Navigate to any endpoint in your browser
## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### 🔐 Authentication Endpoints

| Method | Endpoint | Description | Access | Body Parameters |
|--------|----------|-------------|---------|-----------------|
| `POST` | `/api/auth/register/` | User registration | Public | `username`, `email`, `password`, `password_confirm`, `first_name`, `last_name`, `role` |
| `POST` | `/api/auth/login/` | User login | Public | `email`, `password` |
| `POST` | `/api/auth/logout/` | User logout | Authenticated | `refresh_token` |
| `POST` | `/api/auth/token/refresh/` | Refresh JWT token | Public | `refresh` |
| `GET` | `/api/auth/profile/` | Get user profile | Authenticated | - |
| `PUT` | `/api/auth/profile/` | Update user profile | Authenticated | `username`, `email`, `first_name`, `last_name` |
| `POST` | `/api/auth/change-password/` | Change password | Authenticated | `old_password`, `new_password`, `new_password_confirm` |
| `GET` | `/api/auth/user-info/` | Current user info | Authenticated | - |

### 👥 User Management Endpoints

| Method | Endpoint | Description | Access | Query Parameters |
|--------|----------|-------------|---------|------------------|
| `GET` | `/api/users/` | List all users | Authenticated | `search`, `role`, `is_active` |
| `POST` | `/api/users/` | Create new user | **Admin only** | `username`, `email`, `password`, `password_confirm`, `first_name`, `last_name`, `role`, `is_active` |
| `GET` | `/api/users/{id}/` | Get user details | Owner or Admin | - |
| `PUT` | `/api/users/{id}/` | Update user | Owner or Admin | `username`, `email`, `first_name`, `last_name`, `role`, `is_active` |
| `PATCH` | `/api/users/{id}/` | Partial update | Owner or Admin | Any of the above fields |
| `DELETE` | `/api/users/{id}/` | Delete user | **Admin only** | - |
| `GET` | `/api/users/stats/` | User statistics | **Admin only** | - |
| `POST` | `/api/users/{id}/toggle-status/` | Toggle user status | **Admin only** | - |

### 📂 Category Management (Admin & Moderator Only)

| Method | Endpoint | Description | Access | Parameters |
|--------|----------|-------------|---------|------------|
| `GET` | `/api/categories/` | List categories | **Admin & Moderator** | `search`, `ordering` |
| `POST` | `/api/categories/` | Create category | **Admin & Moderator** | `name`, `description`, `is_active` |
| `GET` | `/api/categories/{id}/` | Category details | **Admin & Moderator** | - |
| `PUT` | `/api/categories/{id}/` | Update category | **Admin & Moderator** | `name`, `description`, `is_active` |
| `PATCH` | `/api/categories/{id}/` | Partial update | **Admin & Moderator** | Any of the above fields |
| `DELETE` | `/api/categories/{id}/` | Soft delete category | **Admin & Moderator** | - |
| `GET` | `/api/categories/stats/` | Category statistics | **Admin & Moderator** | - |
| `POST` | `/api/categories/{id}/toggle-status/` | Toggle status | **Admin & Moderator** | - |

### 📦 Product Management

| Method | Endpoint | Description | Access | Parameters |
|--------|----------|-------------|---------|------------|
| `GET` | `/api/products/` | List products | All authenticated | `search`, `ordering`, `min_price`, `max_price`, `in_stock` |
| `POST` | `/api/products/` | Create product | **Admin & Moderator** | `name`, `description`, `category`, `price`, `stock_quantity`, `sku`, `is_active` |
| `GET` | `/api/products/{id}/` | Product details | All authenticated | - |
| `PUT` | `/api/products/{id}/` | Update product | **Admin & Moderator** | `name`, `description`, `category`, `price`, `stock_quantity`, `sku`, `is_active` |
| `PATCH` | `/api/products/{id}/` | Partial update | **Admin & Moderator** | Any of the above fields |
| `DELETE` | `/api/products/{id}/` | Soft delete product | **Admin & Moderator** | - |
| `GET` | `/api/products/stats/` | Product statistics | All authenticated* | - |
| `POST` | `/api/products/{id}/toggle-status/` | Toggle status | **Admin & Moderator** | - |

> **Note**: *Product stats show full details for Admin/Moderator, basic stats for Users

## 🔑 Authentication

### JWT Token Usage
Include the JWT token in the Authorization header:
```http
Authorization: Bearer <your_access_token>
```

### Token Response Format
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "user123",
    "role": "user",
    "full_name": "John Doe"
  }
}
```

## 🛡️ Permissions

### Role-based Access Matrix

| Resource | Admin | Moderator | User |
|----------|-------|-----------|------|
| **Users** | Full CRUD | Read Only | Own Profile Only |
| **Categories** | Full CRUD | Full CRUD | No Access |
| **Products** | Full CRUD | Full CRUD | Read Only |
| **Statistics** | All Stats | Product/Category Stats | Basic Product Stats |
| **Admin Panel** | ✅ Full Access | ❌ No Access | ❌ No Access |

### Permission Classes
1. **IsAdminRole**: Admin users only
2. **IsAdminOrModerator**: Admin or Moderator users  
3. **IsOwnerOrAdmin**: User owns resource or is Admin
4. **IsOwnerOrAdminOrModerator**: Extended access for Moderators
5. **IsAdminOrReadOnly**: Admin write access, others read-only
6. **IsAdminOrModeratorForProducts**: Product-specific permissions
| GET | `/api/` | API overview and documentation | Public |

## Database Configuration

### PostgreSQL (Production)
Set environment variables:
```bash
export DATABASE_URL=postgresql://username:password@localhost/dbname
export DB_NAME=user_auth_db
export DB_USER=postgres  
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
```

### SQLite (Development - Default)
No configuration needed. Uses `db.sqlite3` file.

## Installation and Setup

### 1. Clone and Setup
```bash
cd User_auth
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# For SQLite (default)
python manage.py makemigrations
python manage.py migrate

# For PostgreSQL (optional)
# Set DATABASE_URL environment variable first
python manage.py makemigrations
python manage.py migrate
```

## 💡 Usage Examples

### 1. User Registration
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "strongpassword123",
    "password_confirm": "strongpassword123",
    "role": "user"
  }'
```

### 2. User Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "strongpassword123"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
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

### 3. List Products (All Users)
```bash
curl -X GET "http://127.0.0.1:8000/api/products/?search=phone&min_price=100&max_price=1000&in_stock=true" \
  -H "Authorization: Bearer <your_access_token>"
```

### 4. Create Category (Admin/Moderator Only)
```bash
curl -X POST http://127.0.0.1:8000/api/categories/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electronics",
    "description": "Electronic devices and gadgets",
    "is_active": true
  }'
```

### 5. Create Product (Admin/Moderator Only)
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15",
    "description": "Latest iPhone model",
    "category": 1,
    "price": "999.99",
    "stock_quantity": 50,
    "sku": "IPHONE15-001",
    "is_active": true
  }'
```

### 6. Get User Statistics (Admin Only)
```bash
curl -X GET http://127.0.0.1:8000/api/users/stats/ \
  -H "Authorization: Bearer <admin_token>"
```

**Response:**
```json
{
  "stats": {
    "total_users": 25,
    "active_users": 23,
    "inactive_users": 2,
    "admin_users": 1,
    "moderator_users": 3,
    "regular_users": 21,
    "recent_registrations": 5
  }
}
```

## 🗂️ Project Structure

```
User_auth/
├── authentication/          # 🔐 Authentication & JWT
│   ├── models.py           # Custom User model
│   ├── serializers.py      # Auth serializers
│   ├── views.py            # Auth views (class-based)
│   ├── permissions.py      # 6 permission classes
│   ├── utils.py            # Validation utilities
│   ├── urls.py             # Auth endpoints
│   └── admin.py            # User admin config
├── users/                  # 👥 User Management
│   ├── serializers.py      # User CRUD serializers
│   ├── views.py            # User CRUD views
│   └── urls.py             # User endpoints
├── products/               # 📦 Product & Category Management
│   ├── models.py           # Category & Product models
│   ├── serializers.py      # Product/Category serializers
│   ├── views.py            # Product/Category views
│   ├── urls.py             # Product endpoints
│   └── admin.py            # Product admin config
├── user_auth_project/      # ⚙️ Main Project
│   ├── settings.py         # Django settings
│   └── urls.py             # Main URL routing
├── requirements.txt        # 📋 Dependencies
├── manage.py              # 🚀 Django management
├── README.md              # 📖 This documentation
└── PROJECT_SUMMARY.md     # 📊 Architecture summary
```

## 🔧 Development

### Database Configuration
The project supports both SQLite (development) and PostgreSQL (production):

**PostgreSQL Setup (Recommended for production):**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Environment Variables
Create a `.env` file:
```env
SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost/dbname
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Running Tests
```bash
python manage.py test
```

### Code Quality
The project follows:
- **PEP 8** style guidelines
- **Django best practices**
- **REST API conventions**
- **Class-based view patterns**
- **DRY principles**

## 📦 Dependencies

```txt
Django==5.2.4
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.4.0
psycopg2-binary==2.9.9
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure production database
- [ ] Set up environment variables
- [ ] Configure static files
- [ ] Set up CORS properly
- [ ] Configure allowed hosts
- [ ] Set up SSL/HTTPS
- [ ] Configure logging

### Docker Support (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For support, email [your-email@example.com] or create an issue in the repository.

## ✨ Features Roadmap

- [ ] Email verification
- [ ] Password reset functionality
- [ ] API rate limiting
- [ ] Advanced filtering options
- [ ] Export functionality
- [ ] API versioning
- [ ] Swagger/OpenAPI documentation
- [ ] Redis caching
- [ ] Background tasks with Celery

---

**Built with ❤️ using Django REST Framework**

{
    "name": "New Gadget",
    "description": "Latest tech gadget",
    "category_id": 1,
    "price": "199.99",
    "stock_quantity": 25,
    "sku": "GADGET001",
    "is_active": true
}
```

### 6. Try to Access Categories as User (Should Fail)
```bash
GET /api/categories/
Authorization: Bearer {user_jwt_token}
```

Response (403 Forbidden):
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 7. Try to Access Categories as Moderator (Should Succeed)
```bash
GET /api/categories/
Authorization: Bearer {moderator_jwt_token}
```

Response (200 OK):
```json
{
    "count": 5,
    "results": [...]
}
```

### 8. Get Product Statistics
```bash
GET /api/products/stats/
Authorization: Bearer {jwt_token}
```

Admin/Moderator Response:
```json
{
    "stats": {
        "total_products": 10,
        "products_in_stock": 8,
        "products_out_of_stock": 2,
        "total_products_including_inactive": 12,
        "inactive_products": 2,
        "categories_count": 5,
        "average_price": 234.99
    }
}
```

User Response (Limited):
```json
{
    "stats": {
        "total_products": 10,
        "products_in_stock": 8,
        "products_out_of_stock": 2
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
- **Users**: Can perform all CRUD operations on users
- **Categories**: **Full access** - view, create, edit, delete categories
- **Products**: **Full access** - view, create, edit, delete products  
- **Statistics**: Access to all statistics endpoints
- **Status Management**: Can toggle user/category/product status
- **Special Access**: Can create admin users, access admin-only endpoints

### Moderator Role (`moderator`)
- **Users**: **NO ACCESS** - cannot manage users
- **Categories**: **Full access** - view, create, edit, delete categories
- **Products**: **Full access** - view, create, edit, delete products
- **Statistics**: Access to full category/product statistics
- **Status Management**: Can toggle category/product status
- **Restrictions**: Cannot manage users or access user management endpoints

### User Role (`user`)
- **Users**: Can view their own profile and update their own information
- **Categories**: **NO ACCESS** - completely blocked from category endpoints
- **Products**: **Read-only access** - can view products but cannot create/edit/delete
- **Statistics**: Limited access to basic product statistics only
- **Status Management**: Cannot toggle any status
- **Restrictions**: Cannot access admin-only endpoints, cannot manage other users

## Permission Matrix

| Feature | Admin | Moderator | User |
|---------|-------|-----------|------|
| View own profile | ✅ | ✅ | ✅ |
| Edit own profile | ✅ | ✅ | ✅ |
| View other users | ✅ | ❌ | ❌ |
| Create users | ✅ | ❌ | ❌ |
| Edit other users | ✅ | ❌ | ❌ |
| Delete users | ✅ | ❌ | ❌ |
| View categories | ✅ | ✅ | ❌ |
| Create categories | ✅ | ✅ | ❌ |
| Edit categories | ✅ | ✅ | ❌ |
| Delete categories | ✅ | ✅ | ❌ |
| View products | ✅ | ✅ | ✅ |
| Create products | ✅ | ✅ | ❌ |
| Edit products | ✅ | ✅ | ❌ |
| Delete products | ✅ | ✅ | ❌ |
| User statistics | ✅ | ❌ | ❌ |
| Category statistics | ✅ | ✅ | ❌ |
| Product statistics (full) | ✅ | ✅ | ❌ |
| Product statistics (basic) | ✅ | ✅ | ✅ |

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
    role = CharField(choices=['admin', 'moderator', 'user'], default='user')
    email = EmailField(unique=True)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_active = BooleanField(default=True)
```

### Category Model
```python
class Category(Model):
    name = CharField(max_length=100, unique=True)
    description = TextField(blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, on_delete=CASCADE)
    is_active = BooleanField(default=True)
```

### Product Model
```python
class Product(Model):
    name = CharField(max_length=200)
    description = TextField(blank=True, null=True)
    category = ForeignKey(Category, on_delete=CASCADE)  # Foreign Key
    price = DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = PositiveIntegerField(default=0)
    sku = CharField(max_length=50, unique=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, on_delete=CASCADE)
    is_active = BooleanField(default=True)
```

## Advanced Features

### Product Filtering & Search
- **Search**: Name, description, SKU, category name
- **Category Filter**: Filter by category ID or name
- **Price Range**: `min_price` and `max_price` parameters
- **Stock Status**: `in_stock` parameter (true/false)
- **Status Filter**: `is_active` parameter
- **Ordering**: By name, price, created_at, stock_quantity

Example:
```bash
GET /api/products/?search=phone&category=1&min_price=100&max_price=1000&in_stock=true&ordering=-price
```

### Soft Delete
- Categories and Products use soft delete (set `is_active=False`)
- Original data is preserved for audit purposes
- Can be reactivated by admins using toggle-status endpoints

## Testing

Test the API using tools like:
- **Postman** or **Insomnia** for API testing
**Built with ❤️ using Django REST Framework**
