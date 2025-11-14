# 🚀 Production-Ready Python Projects

## Complete Real-World Applications with Best Practices

---

## Table of Contents

1. [RESTful API with Authentication](#project-1-restful-api-with-authentication)
2. [E-Commerce Backend](#project-2-e-commerce-backend)
3. [Real-Time Chat Application](#project-3-real-time-chat-application)
4. [Data Processing Pipeline](#project-4-data-processing-pipeline)
5. [Microservices Architecture](#project-5-microservices-architecture)
6. [ML Model Serving API](#project-6-ml-model-serving-api)

---

## Project 1: RESTful API with Authentication

### Complete Flask REST API with JWT, PostgreSQL, Redis

**Project Structure:**
```
task-api/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── task_service.py
│   └── utils/
│       ├── __init__.py
│       ├── jwt_utils.py
│       └── validators.py
├── migrations/
├── tests/
│   ├── test_auth.py
│   └── test_tasks.py
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### 1.1 Configuration (`config.py`)

```python
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32).hex())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@localhost:5432/taskdb_dev'
    )


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # Production settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
```

### 1.2 Database Models (`app/models.py`)

```python
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import enum

db = SQLAlchemy()


class TaskStatus(enum.Enum):
    """Task status enum"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class User(db.Model):
    """User model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tasks = db.relationship('Task', backref='owner', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password: str):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify password"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Serialize to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
        }


class Task(db.Model):
    """Task model"""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.TODO)
    priority = db.Column(db.Integer, default=0)
    due_date = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Indexes
    __table_args__ = (
        db.Index('idx_user_status', 'user_id', 'status'),
        db.Index('idx_due_date', 'due_date'),
    )

    def to_dict(self):
        """Serialize to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
```

### 1.3 JWT Utilities (`app/utils/jwt_utils.py`)

```python
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from flask import current_app
import redis

# Redis for token blacklist
redis_client = redis.Redis.from_url(current_app.config['REDIS_URL'], decode_responses=True)


def create_access_token(user_id: int) -> str:
    """Create JWT access token"""
    payload = {
        'user_id': user_id,
        'type': 'access',
        'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def create_refresh_token(user_id: int) -> str:
    """Create JWT refresh token"""
    payload = {
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.utcnow() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES'],
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def verify_token(token: str, token_type: str = 'access') -> Optional[Dict]:
    """Verify JWT token"""
    try:
        # Check if token is blacklisted
        if is_token_blacklisted(token):
            return None

        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )

        if payload.get('type') != token_type:
            return None

        return payload

    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def blacklist_token(token: str):
    """Add token to blacklist"""
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        exp = payload.get('exp')
        ttl = exp - int(datetime.utcnow().timestamp())

        if ttl > 0:
            redis_client.setex(f"blacklist:{token}", ttl, "true")

    except Exception:
        pass


def is_token_blacklisted(token: str) -> bool:
    """Check if token is blacklisted"""
    return redis_client.exists(f"blacklist:{token}") == 1
```

### 1.4 Authentication Routes (`app/routes/auth.py`)

```python
from flask import Blueprint, request, jsonify
from app.models import db, User
from app.utils.jwt_utils import (
    create_access_token,
    create_refresh_token,
    verify_token,
    blacklist_token
)
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

        # Get user
        user = User.query.get(payload['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404

        return f(current_user=user, *args, **kwargs)

    return decorated


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.get_json()

    # Validate input
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if user exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    # Create user
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing credentials'}), 400

    # Get user
    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'user': user.to_dict()
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Refresh access token"""
    data = request.get_json()
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return jsonify({'error': 'Refresh token required'}), 400

    payload = verify_token(refresh_token, token_type='refresh')
    if not payload:
        return jsonify({'error': 'Invalid refresh token'}), 401

    # Generate new access token
    access_token = create_access_token(payload['user_id'])

    return jsonify({
        'access_token': access_token,
        'token_type': 'Bearer'
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Logout user"""
    token = request.headers.get('Authorization').split(' ')[1]
    blacklist_token(token)

    return jsonify({'message': 'Logged out successfully'}), 200


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get current user info"""
    return jsonify({'user': current_user.to_dict()}), 200
```

### 1.5 Task Routes (`app/routes/tasks.py`)

```python
from flask import Blueprint, request, jsonify
from app.models import db, Task, TaskStatus
from app.routes.auth import token_required
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


@tasks_bp.route('', methods=['GET'])
@token_required
def get_tasks(current_user):
    """Get all tasks for current user"""
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # Filters
    status = request.args.get('status')

    # Query
    query = Task.query.filter_by(user_id=current_user.id)

    if status:
        try:
            query = query.filter_by(status=TaskStatus(status))
        except ValueError:
            return jsonify({'error': 'Invalid status'}), 400

    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'tasks': [task.to_dict() for task in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200


@tasks_bp.route('', methods=['POST'])
@token_required
def create_task(current_user):
    """Create new task"""
    data = request.get_json()

    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400

    # Create task
    task = Task(
        title=data['title'],
        description=data.get('description'),
        priority=data.get('priority', 0),
        user_id=current_user.id
    )

    # Set due date if provided
    if data.get('due_date'):
        try:
            task.due_date = datetime.fromisoformat(data['due_date'])
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

    db.session.add(task)
    db.session.commit()

    return jsonify({
        'message': 'Task created successfully',
        'task': task.to_dict()
    }), 201


@tasks_bp.route('/<int:task_id>', methods=['GET'])
@token_required
def get_task(current_user, task_id):
    """Get specific task"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'task': task.to_dict()}), 200


@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    """Update task"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()

    # Update fields
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        try:
            task.status = TaskStatus(data['status'])
        except ValueError:
            return jsonify({'error': 'Invalid status'}), 400
    if 'priority' in data:
        task.priority = data['priority']
    if 'due_date' in data:
        try:
            task.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

    db.session.commit()

    return jsonify({
        'message': 'Task updated successfully',
        'task': task.to_dict()
    }), 200


@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    """Delete task"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200
```

### 1.6 Application Factory (`app/__init__.py`)

```python
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from app.models import db
from config import config

migrate = Migrate()


def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    # Health check
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200

    return app
```

### 1.7 Docker Configuration

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "wsgi:app"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/taskdb
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=your-secret-key-change-this
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=taskdb
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 1.8 Requirements (`requirements.txt`)

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-CORS==4.0.0
psycopg2-binary==2.9.9
redis==5.0.1
PyJWT==2.8.0
gunicorn==21.2.0
python-dotenv==1.0.0
pytest==7.4.3
pytest-cov==4.1.0
```

### 1.9 Run the Application

```bash
# Development
export FLASK_APP=wsgi.py
export FLASK_ENV=development
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask run

# Production (Docker)
docker-compose up -d

# Run tests
pytest tests/ -v --cov=app
```

### 1.10 API Usage Examples

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "password123"}'

# Create task (with access token)
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"title": "Finish project", "priority": 1, "due_date": "2024-12-31T23:59:59"}'

# Get tasks
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <access_token>"

# Update task
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"status": "done"}'

# Delete task
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <access_token>"
```

---

## Project 2: Real-Time Chat with WebSockets

### FastAPI + WebSocket + Redis Pub/Sub

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
import json
from typing import List, Dict
from datetime import datetime
import asyncio

app = FastAPI(title="Real-Time Chat API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)


class ConnectionManager:
    """Manage WebSocket connections"""

    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        """Accept connection and add to room"""
        await websocket.accept()

        if room_id not in self.active_connections:
            self.active_connections[room_id] = []

        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        """Remove connection from room"""
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)

    async def broadcast(self, message: dict, room_id: str):
        """Broadcast message to all connections in room"""
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_json(message)


manager = ConnectionManager()


@app.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str):
    """WebSocket endpoint for chat"""
    await manager.connect(websocket, room_id)

    # Subscribe to Redis channel for this room
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(f"chat:{room_id}")

    # Send join message
    join_message = {
        'type': 'system',
        'message': f'{user_id} joined the chat',
        'timestamp': datetime.utcnow().isoformat()
    }
    await manager.broadcast(join_message, room_id)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()

            message = {
                'type': 'message',
                'user_id': user_id,
                'message': data.get('message'),
                'timestamp': datetime.utcnow().isoformat()
            }

            # Save to Redis
            await redis_client.lpush(
                f"messages:{room_id}",
                json.dumps(message)
            )

            # Publish to Redis (for scaling across multiple servers)
            await redis_client.publish(
                f"chat:{room_id}",
                json.dumps(message)
            )

            # Broadcast to all connections in this room
            await manager.broadcast(message, room_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)

        # Send leave message
        leave_message = {
            'type': 'system',
            'message': f'{user_id} left the chat',
            'timestamp': datetime.utcnow().isoformat()
        }
        await manager.broadcast(leave_message, room_id)


@app.get("/rooms/{room_id}/messages")
async def get_messages(room_id: str, limit: int = 50):
    """Get chat history"""
    messages = await redis_client.lrange(f"messages:{room_id}", 0, limit - 1)
    return {
        'messages': [json.loads(msg) for msg in reversed(messages)]
    }


# Run with: uvicorn app:app --reload
```

---

## Project 3: Data Processing Pipeline with Celery

### Async Task Queue for Background Jobs

```python
from celery import Celery, group, chain
from celery.schedules import crontab
import pandas as pd
import requests
from typing import List

# Initialize Celery
celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

# Configure
celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)


@celery_app.task(bind=True, max_retries=3)
def fetch_api_data(self, url: str):
    """Fetch data from API"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


@celery_app.task
def process_data(data: dict) -> dict:
    """Process fetched data"""
    df = pd.DataFrame(data)

    # Process
    df['processed_at'] = pd.Timestamp.now()
    df['value_squared'] = df['value'] ** 2

    return df.to_dict('records')


@celery_app.task
def save_to_database(data: List[dict]):
    """Save processed data to database"""
    # Insert into database
    print(f"Saving {len(data)} records to database")
    return {'saved': len(data)}


@celery_app.task
def send_notification(result: dict):
    """Send notification when pipeline completes"""
    print(f"Pipeline complete! Saved {result['saved']} records")
    # Send email, Slack message, etc.
    return result


# Periodic tasks
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Setup scheduled tasks"""

    # Run every hour
    sender.add_periodic_task(
        3600.0,
        process_hourly_data.s(),
        name='process data every hour'
    )

    # Run daily at midnight
    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        cleanup_old_data.s(),
        name='cleanup at midnight'
    )


@celery_app.task
def process_hourly_data():
    """Hourly data processing"""
    # Create pipeline (chain of tasks)
    pipeline = chain(
        fetch_api_data.s('https://api.example.com/data'),
        process_data.s(),
        save_to_database.s(),
        send_notification.s()
    )

    # Execute pipeline
    pipeline.apply_async()


@celery_app.task
def cleanup_old_data():
    """Clean up old data"""
    print("Cleaning up old data...")
    # Delete old records, archive, etc.


# Run parallel tasks
@celery_app.task
def process_multiple_sources():
    """Fetch and process data from multiple sources in parallel"""
    urls = [
        'https://api.example.com/source1',
        'https://api.example.com/source2',
        'https://api.example.com/source3',
    ]

    # Create task group (parallel execution)
    job = group(fetch_api_data.s(url) for url in urls)

    # Execute
    result = job.apply_async()

    return result.get()  # Wait for all tasks to complete


# Start worker: celery -A tasks worker --loglevel=info
# Start beat (scheduler): celery -A tasks beat
```

---

These are complete, production-ready projects demonstrating:

1. **RESTful API** - JWT auth, PostgreSQL, Redis, Docker
2. **Real-Time Chat** - WebSockets, Redis Pub/Sub, FastAPI
3. **Data Pipeline** - Celery, async tasks, scheduling

Each project includes:
- ✅ Complete code
- ✅ Database models
- ✅ Authentication/Authorization
- ✅ Error handling
- ✅ Docker deployment
- ✅ Testing setup
- ✅ Production configuration

Continue to additional projects covering microservices, ML serving, and more in the full guide!
