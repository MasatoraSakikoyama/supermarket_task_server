# supermarket_task_server

FastAPI application for AWS Lambda with Aurora MySQL database.

## Requirements

- Python 3.13+
- pipenv

## Setup

### Install dependencies

```bash
pip install pipenv
pipenv install
```

### Environment variables

Create a `.env` file with the following variables:

```env
DB_HOST=your-aurora-mysql-endpoint.rds.amazonaws.com
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=supermarket
DEBUG=false

# DynamoDB settings
DYNAMODB_TABLE_NAME=user_tokens
DYNAMODB_REGION=ap-northeast-1
DYNAMODB_ENDPOINT_URL=

# JWT settings
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### DynamoDB Table Setup

Create a DynamoDB table with the following configuration:
- Table name: `user_tokens` (or value of `DYNAMODB_TABLE_NAME`)
- Partition key: `user_id` (String)
- Enable TTL on the `ttl` attribute for automatic token expiration

### Database migrations

Run database migrations:

```bash
pipenv run alembic upgrade head
```

Create a new migration:

```bash
pipenv run alembic revision --autogenerate -m "migration message"
```

## Local development

Run the application locally:

```bash
pipenv run uvicorn app.main:app --reload
```

## AWS Lambda deployment

The application uses Mangum as the ASGI adapter for AWS Lambda.
The Lambda handler is exposed as `app.main.handler`.

### Lambda configuration

- Handler: `app.main.handler`
- Runtime: Python 3.13

## API endpoints

### Authentication (No login required)
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token

### Authentication (Login required)
- `POST /auth/logout` - Logout and invalidate token
- `GET /auth/me` - Get current user information

### Shops (Login required)
- `GET /shops` - List all shops
- `GET /shops/{shop_id}` - Get shop by ID
- `POST /shops` - Create a new shop
- `PUT /shops/{shop_id}` - Update a shop
- `DELETE /shops/{shop_id}` - Delete a shop

### Shop Settlements (Login required)
- `GET /shops/{shop_id}/settlements` - List all settlements for a shop
- `GET /shops/{shop_id}/settlements/{settlement_id}` - Get settlement by ID
- `POST /shops/{shop_id}/settlements` - Create a new settlement
- `PUT /shops/{shop_id}/settlements/{settlement_id}` - Update a settlement
- `DELETE /shops/{shop_id}/settlements/{settlement_id}` - Delete a settlement

## Project structure

```
.
├── alembic/                  # Database migrations
│   ├── versions/             # Migration scripts
│   ├── env.py                # Alembic environment
│   └── script.py.mako        # Migration template
├── app/
│   ├── models/               # SQLAlchemy models
│   ├── routers/              # API route handlers
│   ├── schemas/              # Pydantic schemas
│   ├── config.py             # Application configuration
│   ├── database.py           # Database connection
│   └── main.py               # FastAPI application & Lambda handler
├── alembic.ini               # Alembic configuration
├── Pipfile                   # Dependencies (pipenv)
└── README.md
```