# supermarket_task_server

FastAPI application for AWS Lambda with Aurora MySQL database.

## Requirements

- Python 3.12+
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
```

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
- Runtime: Python 3.12

## API endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /items` - List all items
- `GET /items/{item_id}` - Get item by ID
- `POST /items` - Create a new item
- `PUT /items/{item_id}` - Update an item
- `DELETE /items/{item_id}` - Delete an item

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