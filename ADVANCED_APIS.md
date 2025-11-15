# 🔌 Advanced API Development - GraphQL, gRPC & Modern Protocols

## Complete Professional Guide to Modern API Technologies

---

## Table of Contents

1. [GraphQL APIs](#1-graphql-apis)
2. [gRPC and Protocol Buffers](#2-grpc-and-protocol-buffers)
3. [WebSocket APIs](#3-websocket-apis)
4. [API Gateway Patterns](#4-api-gateway-patterns)
5. [API Versioning Strategies](#5-api-versioning-strategies)
6. [Rate Limiting & Throttling](#6-rate-limiting--throttling)
7. [API Documentation (OpenAPI/Swagger)](#7-api-documentation)
8. [API Security Best Practices](#8-api-security-best-practices)

---

## 1. GraphQL APIs

### 1.1 Complete GraphQL Server with Strawberry

```python
from typing import List, Optional
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
from datetime import datetime
import databases
import sqlalchemy

# Database setup
DATABASE_URL = "postgresql://user:password@localhost/dbname"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Database tables
users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(50)),
    sqlalchemy.Column("email", sqlalchemy.String(100)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
)

posts_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(200)),
    sqlalchemy.Column("content", sqlalchemy.Text),
    sqlalchemy.Column("author_id", sqlalchemy.Integer),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
)


# GraphQL Types
@strawberry.type
class User:
    id: int
    username: str
    email: str
    created_at: datetime

    @strawberry.field
    async def posts(self) -> List['Post']:
        """Resolve user's posts"""
        query = posts_table.select().where(posts_table.c.author_id == self.id)
        results = await database.fetch_all(query)
        return [Post(**dict(row)) for row in results]


@strawberry.type
class Post:
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime

    @strawberry.field
    async def author(self) -> User:
        """Resolve post's author"""
        query = users_table.select().where(users_table.c.id == self.author_id)
        result = await database.fetch_one(query)
        return User(**dict(result))


# Input types for mutations
@strawberry.input
class CreateUserInput:
    username: str
    email: str


@strawberry.input
class CreatePostInput:
    title: str
    content: str
    author_id: int


@strawberry.input
class UpdatePostInput:
    id: int
    title: Optional[str] = None
    content: Optional[str] = None


# Queries
@strawberry.type
class Query:
    @strawberry.field
    async def users(self, limit: int = 10, offset: int = 0) -> List[User]:
        """Get all users with pagination"""
        query = users_table.select().limit(limit).offset(offset)
        results = await database.fetch_all(query)
        return [User(**dict(row)) for row in results]

    @strawberry.field
    async def user(self, id: int) -> Optional[User]:
        """Get user by ID"""
        query = users_table.select().where(users_table.c.id == id)
        result = await database.fetch_one(query)
        return User(**dict(result)) if result else None

    @strawberry.field
    async def posts(
        self,
        limit: int = 10,
        offset: int = 0,
        author_id: Optional[int] = None
    ) -> List[Post]:
        """Get posts with optional filtering"""
        query = posts_table.select().limit(limit).offset(offset)

        if author_id:
            query = query.where(posts_table.c.author_id == author_id)

        results = await database.fetch_all(query)
        return [Post(**dict(row)) for row in results]

    @strawberry.field
    async def search_posts(self, keyword: str) -> List[Post]:
        """Search posts by keyword"""
        query = posts_table.select().where(
            posts_table.c.title.contains(keyword) |
            posts_table.c.content.contains(keyword)
        )
        results = await database.fetch_all(query)
        return [Post(**dict(row)) for row in results]


# Mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, input: CreateUserInput) -> User:
        """Create new user"""
        query = users_table.insert().values(
            username=input.username,
            email=input.email,
            created_at=datetime.utcnow()
        )
        user_id = await database.execute(query)

        # Return created user
        return User(
            id=user_id,
            username=input.username,
            email=input.email,
            created_at=datetime.utcnow()
        )

    @strawberry.mutation
    async def create_post(self, input: CreatePostInput) -> Post:
        """Create new post"""
        query = posts_table.insert().values(
            title=input.title,
            content=input.content,
            author_id=input.author_id,
            created_at=datetime.utcnow()
        )
        post_id = await database.execute(query)

        return Post(
            id=post_id,
            title=input.title,
            content=input.content,
            author_id=input.author_id,
            created_at=datetime.utcnow()
        )

    @strawberry.mutation
    async def update_post(self, input: UpdatePostInput) -> Post:
        """Update existing post"""
        values = {}
        if input.title:
            values['title'] = input.title
        if input.content:
            values['content'] = input.content

        query = posts_table.update().where(
            posts_table.c.id == input.id
        ).values(**values)

        await database.execute(query)

        # Return updated post
        query = posts_table.select().where(posts_table.c.id == input.id)
        result = await database.fetch_one(query)
        return Post(**dict(result))

    @strawberry.mutation
    async def delete_post(self, id: int) -> bool:
        """Delete post"""
        query = posts_table.delete().where(posts_table.c.id == id)
        await database.execute(query)
        return True


# Subscriptions (Real-time updates)
@strawberry.type
class Subscription:
    @strawberry.subscription
    async def new_posts(self) -> Post:
        """Subscribe to new posts"""
        # In production, use Redis Pub/Sub or similar
        import asyncio
        while True:
            await asyncio.sleep(5)
            # Check for new posts and yield them
            query = posts_table.select().order_by(
                posts_table.c.created_at.desc()
            ).limit(1)
            result = await database.fetch_one(query)
            if result:
                yield Post(**dict(result))


# Create schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)

# FastAPI integration
app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Add GraphQL route
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Run with: uvicorn app:app --reload
# GraphQL playground: http://localhost:8000/graphql
```

### 1.2 GraphQL Client Usage

```python
import httpx
import asyncio

class GraphQLClient:
    """GraphQL client for making queries"""

    def __init__(self, url: str):
        self.url = url
        self.client = httpx.AsyncClient()

    async def query(self, query: str, variables: dict = None):
        """Execute GraphQL query"""
        response = await self.client.post(
            self.url,
            json={'query': query, 'variables': variables or {}}
        )
        return response.json()

    async def close(self):
        await self.client.aclose()


# Usage examples
async def main():
    client = GraphQLClient('http://localhost:8000/graphql')

    # Query users
    query = """
    query GetUsers($limit: Int!) {
        users(limit: $limit) {
            id
            username
            email
            posts {
                id
                title
            }
        }
    }
    """
    result = await client.query(query, {'limit': 5})
    print(result)

    # Create user mutation
    mutation = """
    mutation CreateUser($input: CreateUserInput!) {
        createUser(input: $input) {
            id
            username
            email
        }
    }
    """
    result = await client.query(mutation, {
        'input': {
            'username': 'john_doe',
            'email': 'john@example.com'
        }
    })
    print(result)

    # Search posts
    search_query = """
    query SearchPosts($keyword: String!) {
        searchPosts(keyword: $keyword) {
            id
            title
            content
            author {
                username
            }
        }
    }
    """
    result = await client.query(search_query, {'keyword': 'python'})
    print(result)

    await client.close()

# Run
asyncio.run(main())
```

---

## 2. gRPC and Protocol Buffers

### 2.1 Protocol Buffer Definition (.proto)

```protobuf
// user_service.proto
syntax = "proto3";

package userservice;

// User message
message User {
    int32 id = 1;
    string username = 2;
    string email = 3;
    string created_at = 4;
}

// Request/Response messages
message GetUserRequest {
    int32 id = 1;
}

message GetUserResponse {
    User user = 1;
}

message CreateUserRequest {
    string username = 1;
    string email = 2;
}

message CreateUserResponse {
    User user = 1;
}

message ListUsersRequest {
    int32 page_size = 1;
    int32 page_number = 2;
}

message ListUsersResponse {
    repeated User users = 1;
    int32 total = 2;
}

message UpdateUserRequest {
    int32 id = 1;
    string username = 2;
    string email = 3;
}

message UpdateUserResponse {
    User user = 1;
}

message DeleteUserRequest {
    int32 id = 1;
}

message DeleteUserResponse {
    bool success = 1;
}

// Service definition
service UserService {
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
    rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
    rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
    rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);
    rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);

    // Server streaming
    rpc StreamUsers(ListUsersRequest) returns (stream User);

    // Client streaming
    rpc CreateUsers(stream CreateUserRequest) returns (CreateUserResponse);

    // Bidirectional streaming
    rpc Chat(stream ChatMessage) returns (stream ChatMessage);
}

message ChatMessage {
    string user_id = 1;
    string message = 2;
    string timestamp = 3;
}
```

### 2.2 gRPC Server Implementation

```python
# Generate Python code from proto:
# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user_service.proto

import grpc
from concurrent import futures
import user_service_pb2
import user_service_pb2_grpc
from datetime import datetime
import asyncio
from typing import Iterator

class UserServiceServicer(user_service_pb2_grpc.UserServiceServicer):
    """gRPC User Service implementation"""

    def __init__(self):
        # In production, use real database
        self.users = {}
        self.next_id = 1

    def GetUser(self, request, context):
        """Get user by ID"""
        user_id = request.id

        if user_id not in self.users:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'User {user_id} not found')
            return user_service_pb2.GetUserResponse()

        user = self.users[user_id]
        return user_service_pb2.GetUserResponse(user=user)

    def CreateUser(self, request, context):
        """Create new user"""
        user = user_service_pb2.User(
            id=self.next_id,
            username=request.username,
            email=request.email,
            created_at=datetime.utcnow().isoformat()
        )

        self.users[self.next_id] = user
        self.next_id += 1

        return user_service_pb2.CreateUserResponse(user=user)

    def ListUsers(self, request, context):
        """List users with pagination"""
        page_size = request.page_size or 10
        page_number = request.page_number or 1

        start = (page_number - 1) * page_size
        end = start + page_size

        users_list = list(self.users.values())[start:end]

        return user_service_pb2.ListUsersResponse(
            users=users_list,
            total=len(self.users)
        )

    def UpdateUser(self, request, context):
        """Update user"""
        user_id = request.id

        if user_id not in self.users:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'User {user_id} not found')
            return user_service_pb2.UpdateUserResponse()

        user = self.users[user_id]
        if request.username:
            user.username = request.username
        if request.email:
            user.email = request.email

        return user_service_pb2.UpdateUserResponse(user=user)

    def DeleteUser(self, request, context):
        """Delete user"""
        user_id = request.id

        if user_id in self.users:
            del self.users[user_id]
            return user_service_pb2.DeleteUserResponse(success=True)

        return user_service_pb2.DeleteUserResponse(success=False)

    def StreamUsers(self, request, context):
        """Server streaming - stream all users"""
        for user in self.users.values():
            yield user

    def CreateUsers(self, request_iterator, context):
        """Client streaming - receive multiple users"""
        count = 0
        last_user = None

        for request in request_iterator:
            user = user_service_pb2.User(
                id=self.next_id,
                username=request.username,
                email=request.email,
                created_at=datetime.utcnow().isoformat()
            )
            self.users[self.next_id] = user
            self.next_id += 1
            count += 1
            last_user = user

        return user_service_pb2.CreateUserResponse(user=last_user)

    def Chat(self, request_iterator, context):
        """Bidirectional streaming - chat"""
        for message in request_iterator:
            # Echo back with timestamp
            response = user_service_pb2.ChatMessage(
                user_id=message.user_id,
                message=f"Echo: {message.message}",
                timestamp=datetime.utcnow().isoformat()
            )
            yield response


def serve():
    """Start gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(), server
    )

    server.add_insecure_port('[::]:50051')
    server.start()

    print("gRPC Server started on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
```

### 2.3 gRPC Client

```python
import grpc
import user_service_pb2
import user_service_pb2_grpc

class UserServiceClient:
    """gRPC client for UserService"""

    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = user_service_pb2_grpc.UserServiceStub(self.channel)

    def get_user(self, user_id: int):
        """Get user by ID"""
        request = user_service_pb2.GetUserRequest(id=user_id)
        response = self.stub.GetUser(request)
        return response.user

    def create_user(self, username: str, email: str):
        """Create new user"""
        request = user_service_pb2.CreateUserRequest(
            username=username,
            email=email
        )
        response = self.stub.CreateUser(request)
        return response.user

    def list_users(self, page_size: int = 10, page_number: int = 1):
        """List users"""
        request = user_service_pb2.ListUsersRequest(
            page_size=page_size,
            page_number=page_number
        )
        response = self.stub.ListUsers(request)
        return response.users, response.total

    def stream_users(self):
        """Stream all users (server streaming)"""
        request = user_service_pb2.ListUsersRequest()

        for user in self.stub.StreamUsers(request):
            print(f"Received user: {user.username}")
            yield user

    def create_users_batch(self, users_data: list):
        """Create multiple users (client streaming)"""
        def request_generator():
            for data in users_data:
                yield user_service_pb2.CreateUserRequest(**data)

        response = self.stub.CreateUsers(request_generator())
        return response.user

    def chat(self, messages: list):
        """Bidirectional streaming chat"""
        def message_generator():
            for msg in messages:
                yield user_service_pb2.ChatMessage(**msg)

        responses = self.stub.Chat(message_generator())

        for response in responses:
            print(f"Received: {response.message}")

    def close(self):
        """Close channel"""
        self.channel.close()


# Usage
client = UserServiceClient()

# Create user
user = client.create_user('john_doe', 'john@example.com')
print(f"Created user: {user.id} - {user.username}")

# Get user
user = client.get_user(1)
print(f"User: {user.username} ({user.email})")

# List users
users, total = client.list_users(page_size=5)
print(f"Found {total} users")

# Server streaming
for user in client.stream_users():
    print(f"Streamed: {user.username}")

# Client streaming - batch create
users_to_create = [
    {'username': 'user1', 'email': 'user1@example.com'},
    {'username': 'user2', 'email': 'user2@example.com'},
    {'username': 'user3', 'email': 'user3@example.com'},
]
last_user = client.create_users_batch(users_to_create)
print(f"Batch created, last user: {last_user.username}")

# Bidirectional streaming
messages = [
    {'user_id': '1', 'message': 'Hello!'},
    {'user_id': '1', 'message': 'How are you?'},
]
client.chat(messages)

client.close()
```

---

## 3. WebSocket APIs

### 3.1 Professional WebSocket Server

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import asyncio
from datetime import datetime

app = FastAPI()


class ConnectionManager:
    """Manage WebSocket connections with rooms and authentication"""

    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}
        self.user_metadata: Dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, room_id: str, user_id: str):
        """Connect user to room"""
        await websocket.accept()

        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}

        self.active_connections[room_id][user_id] = websocket
        self.user_metadata[user_id] = {
            'room_id': room_id,
            'connected_at': datetime.utcnow().isoformat()
        }

    def disconnect(self, room_id: str, user_id: str):
        """Disconnect user from room"""
        if room_id in self.active_connections:
            self.active_connections[room_id].pop(user_id, None)

            # Clean up empty rooms
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

        self.user_metadata.pop(user_id, None)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific connection"""
        await websocket.send_text(message)

    async def broadcast_to_room(self, room_id: str, message: dict, exclude_user: str = None):
        """Broadcast message to all users in room"""
        if room_id in self.active_connections:
            for user_id, connection in self.active_connections[room_id].items():
                if user_id != exclude_user:
                    await connection.send_json(message)

    async def broadcast_to_all(self, message: dict):
        """Broadcast to all connected users"""
        for room_connections in self.active_connections.values():
            for connection in room_connections.values():
                await connection.send_json(message)

    def get_room_users(self, room_id: str) -> List[str]:
        """Get list of users in room"""
        return list(self.active_connections.get(room_id, {}).keys())

    def get_user_count(self, room_id: str) -> int:
        """Get number of users in room"""
        return len(self.active_connections.get(room_id, {}))


manager = ConnectionManager()


@app.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str):
    """WebSocket endpoint with rooms"""
    await manager.connect(websocket, room_id, user_id)

    # Send join notification
    await manager.broadcast_to_room(
        room_id,
        {
            'type': 'user_joined',
            'user_id': user_id,
            'message': f'{user_id} joined the room',
            'users_count': manager.get_user_count(room_id),
            'timestamp': datetime.utcnow().isoformat()
        }
    )

    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Process based on message type
            msg_type = message_data.get('type', 'message')

            if msg_type == 'message':
                # Broadcast chat message
                await manager.broadcast_to_room(
                    room_id,
                    {
                        'type': 'message',
                        'user_id': user_id,
                        'message': message_data.get('message'),
                        'timestamp': datetime.utcnow().isoformat()
                    }
                )

            elif msg_type == 'typing':
                # Broadcast typing indicator
                await manager.broadcast_to_room(
                    room_id,
                    {
                        'type': 'typing',
                        'user_id': user_id,
                        'is_typing': message_data.get('is_typing', False)
                    },
                    exclude_user=user_id
                )

            elif msg_type == 'get_users':
                # Send list of users in room
                users = manager.get_room_users(room_id)
                await manager.send_personal_message(
                    json.dumps({
                        'type': 'users_list',
                        'users': users
                    }),
                    websocket
                )

    except WebSocketDisconnect:
        manager.disconnect(room_id, user_id)

        # Send leave notification
        await manager.broadcast_to_room(
            room_id,
            {
                'type': 'user_left',
                'user_id': user_id,
                'message': f'{user_id} left the room',
                'users_count': manager.get_user_count(room_id),
                'timestamp': datetime.utcnow().isoformat()
            }
        )


@app.get("/rooms/{room_id}/users")
async def get_room_users(room_id: str):
    """Get users in room"""
    return {
        'room_id': room_id,
        'users': manager.get_room_users(room_id),
        'count': manager.get_user_count(room_id)
    }


# WebSocket client example (JavaScript)
"""
const ws = new WebSocket('ws://localhost:8000/ws/room1/user123');

ws.onopen = () => {
    console.log('Connected');

    // Send message
    ws.send(JSON.stringify({
        type: 'message',
        message: 'Hello everyone!'
    }));

    // Send typing indicator
    ws.send(JSON.stringify({
        type: 'typing',
        is_typing: true
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

ws.onclose = () => {
    console.log('Disconnected');
};
"""
```

---

## 4. API Gateway Pattern

### 4.1 Simple API Gateway

```python
from fastapi import FastAPI, Request, HTTPException
import httpx
from typing import Dict
import time

app = FastAPI(title="API Gateway")


class APIGateway:
    """API Gateway for routing requests to microservices"""

    def __init__(self):
        self.services = {
            'users': 'http://localhost:8001',
            'posts': 'http://localhost:8002',
            'comments': 'http://localhost:8003',
        }
        self.client = httpx.AsyncClient()
        self.rate_limits: Dict[str, list] = {}

    async def route_request(
        self,
        service: str,
        path: str,
        method: str = 'GET',
        **kwargs
    ):
        """Route request to appropriate microservice"""
        if service not in self.services:
            raise HTTPException(status_code=404, detail=f"Service {service} not found")

        base_url = self.services[service]
        url = f"{base_url}{path}"

        # Forward request
        response = await self.client.request(method, url, **kwargs)
        return response.json()

    def check_rate_limit(self, client_id: str, limit: int = 100, window: int = 60):
        """Check rate limit (requests per window)"""
        now = time.time()

        if client_id not in self.rate_limits:
            self.rate_limits[client_id] = []

        # Remove old requests outside window
        self.rate_limits[client_id] = [
            req_time for req_time in self.rate_limits[client_id]
            if now - req_time < window
        ]

        # Check limit
        if len(self.rate_limits[client_id]) >= limit:
            return False

        # Add current request
        self.rate_limits[client_id].append(now)
        return True


gateway = APIGateway()


@app.get("/{service}/{path:path}")
async def gateway_get(service: str, path: str, request: Request):
    """Gateway GET requests"""
    # Check rate limit
    client_id = request.client.host
    if not gateway.check_rate_limit(client_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Route request
    result = await gateway.route_request(
        service,
        f"/{path}",
        params=dict(request.query_params)
    )

    return result


@app.post("/{service}/{path:path}")
async def gateway_post(service: str, path: str, request: Request):
    """Gateway POST requests"""
    client_id = request.client.host
    if not gateway.check_rate_limit(client_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    body = await request.json()

    result = await gateway.route_request(
        service,
        f"/{path}",
        method='POST',
        json=body
    )

    return result


# Health check
@app.get("/health")
async def health():
    """Check health of all services"""
    health_status = {}

    for service, url in gateway.services.items():
        try:
            response = await gateway.client.get(f"{url}/health", timeout=2.0)
            health_status[service] = {
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            health_status[service] = {
                'status': 'unhealthy',
                'error': str(e)
            }

    return health_status
```

---

This is a comprehensive guide to modern API development covering GraphQL, gRPC, WebSockets, and API Gateway patterns. These are production-ready examples used in real-world applications!

**Key Takeaways**:
- **GraphQL**: Flexible queries, no over-fetching, real-time subscriptions
- **gRPC**: High performance, strong typing, multiple streaming modes
- **WebSockets**: Real-time bidirectional communication
- **API Gateway**: Centralized routing, rate limiting, service orchestration

Use these patterns to build modern, scalable API architectures!
