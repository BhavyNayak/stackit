# StackIt - Q&A Platform API

A comprehensive Q&A platform built with FastAPI, featuring JWT authentication, async database operations, and full CRUD functionality.

## Team Information
**Team Name**: HackNova (4518)

### Members
- **Satyadevsinh Rathod** - satyadev94095@gmail.com
- **Bhavya Nayak** - nayakbhavy132@gmail.com  
- **Aryan Panchal** - aryu9815@gmail.com

## Features

- 🔐 **JWT Authentication** - Secure user authentication with JWT tokens
- 👥 **User Management** - Complete user CRUD operations with role-based access
- ❓ **Question Management** - Create, read, update, delete questions with search functionality
- 💬 **Answer Management** - Answer questions, mark accepted answers, and manage responses
- 🗄️ **Async Database** - PostgreSQL with async SQLAlchemy operations
- 📝 **Pydantic Schemas** - Type-safe request/response validation
- 🔒 **Role-Based Access** - User roles (guest, user, admin) with proper permissions
- 📊 **Consistent API Responses** - Standardized response format across all endpoints
- 🚀 **FastAPI** - High-performance API with automatic documentation

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Database
- **JWT** - JSON Web Tokens for authentication
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server
- **Passlib** - Password hashing
- **Python-jose** - JWT implementation

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd StackIt
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

4. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   # Edit .env with your database credentials and secret key
   ```

5. **Set up PostgreSQL database**
   - Create a PostgreSQL database
   - Update the DATABASE_URL in your .env file

6. **Run the application**
   ```bash
   python main.py
   ```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - Login and get JWT token
- `GET /api/users/me` - Get current user info

### Users
- `GET /api/users/` - Get all users (admin only)
- `GET /api/users/{user_id}` - Get user by ID
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user (admin only)

### Questions
- `POST /api/questions/` - Create a new question
- `GET /api/questions/` - Get all questions (with search)
- `GET /api/questions/my-questions` - Get current user's questions
- `GET /api/questions/{question_id}` - Get question by ID
- `PUT /api/questions/{question_id}` - Update question
- `DELETE /api/questions/{question_id}` - Delete question
- `GET /api/questions/user/{user_id}` - Get questions by user

### Answers
- `POST /api/answers/` - Create a new answer
- `GET /api/answers/question/{question_id}` - Get answers for a question
- `GET /api/answers/my-answers` - Get current user's answers
- `GET /api/answers/{answer_id}` - Get answer by ID
- `PUT /api/answers/{answer_id}` - Update answer
- `DELETE /api/answers/{answer_id}` - Delete answer
- `POST /api/answers/{answer_id}/accept` - Mark answer as accepted
- `GET /api/answers/user/{user_id}` - Get answers by user
- `GET /api/answers/question/{question_id}/accepted` - Get accepted answer for question

## Response Format

All API responses follow this consistent format:

```json
{
  "status": 200,
  "message": "Operation successfully done",
  "data": {
    // Response data here
  }
}
```

## Authentication

Most endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## User Roles

- **guest** - Basic access
- **user** - Can create questions and answers
- **admin** - Full access, can manage users

## Database Schema

### Users Table
- `user_id` (UUID, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `password` (String, Hashed)
- `role` (Enum: guest, user, admin)
- `created_at` (DateTime)

### Questions Table
- `question_id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key)
- `title` (String)
- `description` (Text)
- `created_at` (DateTime)
- `updated_at` (DateTime, Nullable)

### Answers Table
- `answer_id` (UUID, Primary Key)
- `question_id` (UUID, Foreign Key)
- `user_id` (UUID, Foreign Key)
- `content` (Text)
- `is_accepted` (Boolean)
- `created_at` (DateTime)

## Testing with Postman

1. **Register a user**
   ```
   POST http://localhost:8000/api/users/register
   Content-Type: application/json
   
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "password123",
     "role": "user"
   }
   ```

2. **Login to get JWT token**
   ```
   POST http://localhost:8000/api/users/login
   Content-Type: application/json
   
   {
     "email": "test@example.com",
     "password": "password123"
   }
   ```

3. **Use the token for authenticated requests**
   ```
   Authorization: Bearer <your-jwt-token>
   ```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost/database_name
ASYNC_DATABASE_URL=postgresql+asyncpg://username:password@localhost/database_name

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

## Development

### Running in Development Mode
```bash
python main.py
```

### Running with Uvicorn
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Project Structure

```
stackit/
├── main.py                 # FastAPI application entry point
├── models.py              # SQLAlchemy models
├── consts.py              # Constants and enums
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
├── README.md             # This file
├── database/             # Database services
│   ├── users.py          # User service
│   ├── question_service.py # Question service
│   └── answer_service.py # Answer service
├── routes/               # API routes
│   ├── user_routes.py    # User endpoints
│   ├── question_routes.py # Question endpoints
│   └── answer_routes.py  # Answer endpoints
├── schemas/              # Pydantic schemas
│   ├── user_schemas.py   # User request/response models
│   ├── question_schemas.py # Question request/response models
│   ├── answer_schemas.py # Answer request/response models
│   └── response_schemas.py # Common response format
└── utils/                # Utility functions
    ├── database_helper.py # Database configuration
    ├── auth_helper.py    # JWT authentication
    └── exception_handler.py # Exception handling
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
