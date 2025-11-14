# 🎓 Professional Python Developer Path
## From Beginner to Industry Expert - Complete Mastery

This comprehensive guide covers EVERYTHING you need to become a professional Python developer who can get hired and deliver production systems.

---

# PART 1: ADVANCED PYTHON FUNDAMENTALS

## Module 13: Advanced Functions and Decorators

### 13.1 Advanced Decorator Patterns

```python
import functools
import time
from typing import Callable, Any

# Professional decorator with arguments
def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry a function on failure"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

# Class-based decorators
class RateLimiter:
    """Professional rate limiting decorator"""
    def __init__(self, max_calls: int, time_window: float):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls
            self.calls = [call for call in self.calls
                         if now - call < self.time_window]

            if len(self.calls) >= self.max_calls:
                raise Exception("Rate limit exceeded")

            self.calls.append(now)
            return func(*args, **kwargs)
        return wrapper

# Chaining decorators
@retry(max_attempts=3)
@RateLimiter(max_calls=10, time_window=60)
def api_call(endpoint: str) -> dict:
    """Make API call with retry and rate limiting"""
    # Your API logic here
    pass

# Performance profiling decorator
def profile(func: Callable) -> Callable:
    """Profile function execution time and memory"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import tracemalloc

        tracemalloc.start()
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"\n{func.__name__} Performance:")
        print(f"Time: {end_time - start_time:.4f} seconds")
        print(f"Current memory: {current / 1024**2:.2f} MB")
        print(f"Peak memory: {peak / 1024**2:.2f} MB")

        return result
    return wrapper

# Caching decorator (memoization)
def memoize(func: Callable) -> Callable:
    """Cache function results"""
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fibonacci(n: int) -> int:
    """Optimized fibonacci with caching"""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### 13.2 Context Managers (Advanced)

```python
from contextlib import contextmanager
import threading
import logging

# Professional file handler
@contextmanager
def safe_file_handler(filename: str, mode: str = 'r'):
    """Context manager with error handling and logging"""
    file_handle = None
    try:
        logging.info(f"Opening file: {filename}")
        file_handle = open(filename, mode)
        yield file_handle
    except IOError as e:
        logging.error(f"Error accessing {filename}: {e}")
        raise
    finally:
        if file_handle:
            file_handle.close()
            logging.info(f"Closed file: {filename}")

# Database transaction manager
class DatabaseTransaction:
    """Professional database transaction context manager"""
    def __init__(self, connection):
        self.connection = connection
        self.transaction = None

    def __enter__(self):
        self.transaction = self.connection.begin()
        return self.transaction

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.transaction.rollback()
            logging.error(f"Transaction rolled back: {exc_val}")
            return False
        else:
            self.transaction.commit()
            logging.info("Transaction committed")
            return True

# Thread lock context manager
class ThreadSafeLock:
    """Thread-safe operations context manager"""
    def __init__(self):
        self._lock = threading.Lock()

    def __enter__(self):
        self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()
        return False

# Timer context manager
@contextmanager
def timer(name: str = "Operation"):
    """Time code execution"""
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"{name} took {end - start:.4f} seconds")

# Usage
with timer("Database query"):
    # Your code here
    time.sleep(0.1)
```

### 13.3 Generators and Iterators (Professional)

```python
from typing import Iterator, Generator
import sys

# Memory-efficient data processing
def read_large_file(filename: str, chunk_size: int = 8192) -> Generator[str, None, None]:
    """Read large files efficiently"""
    with open(filename, 'r') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Generator pipeline
def process_data_pipeline(data_source: Iterator) -> Generator:
    """Professional data processing pipeline"""
    # Filter
    filtered = (item for item in data_source if item.get('active'))

    # Transform
    transformed = (transform_item(item) for item in filtered)

    # Aggregate
    for item in transformed:
        yield item

# Infinite generator
def id_generator(start: int = 0) -> Generator[int, None, None]:
    """Generate unique IDs"""
    current = start
    while True:
        yield current
        current += 1

# Batch generator
def batch_generator(iterable: Iterator, batch_size: int) -> Generator:
    """Process data in batches"""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

# Usage example
data = range(1000000)
for batch in batch_generator(data, batch_size=100):
    # Process batch
    process_batch(batch)
```

---

# PART 2: TESTING AND QUALITY ASSURANCE

## Module 14: Professional Testing

### 14.1 Unit Testing with pytest

```python
import pytest
from typing import List
import tempfile
import os

# Test fixtures
@pytest.fixture
def sample_data() -> List[dict]:
    """Provide sample data for tests"""
    return [
        {'id': 1, 'name': 'Alice', 'score': 95},
        {'id': 2, 'name': 'Bob', 'score': 87},
        {'id': 3, 'name': 'Charlie', 'score': 92}
    ]

@pytest.fixture
def temp_file():
    """Create temporary file for testing"""
    fd, path = tempfile.mkstemp()
    yield path
    os.close(fd)
    os.unlink(path)

# Parameterized tests
@pytest.mark.parametrize("input,expected", [
    (5, 120),
    (0, 1),
    (1, 1),
    (3, 6),
])
def test_factorial(input: int, expected: int):
    """Test factorial function with multiple inputs"""
    assert factorial(input) == expected

# Exception testing
def test_division_by_zero():
    """Test exception handling"""
    with pytest.raises(ZeroDivisionError):
        result = 10 / 0

# Mock testing
from unittest.mock import Mock, patch, MagicMock

def test_api_call_with_mock():
    """Test API calls with mocking"""
    # Mock the requests library
    with patch('requests.get') as mock_get:
        # Configure mock
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'data': 'test'}

        # Call function
        result = fetch_api_data('http://api.example.com')

        # Assertions
        assert result == {'data': 'test'}
        mock_get.assert_called_once_with('http://api.example.com')

# Integration tests
class TestUserService:
    """Integration tests for user service"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test database"""
        self.db = create_test_database()
        yield
        self.db.cleanup()

    def test_create_user(self):
        """Test user creation"""
        user = self.db.create_user('test@example.com', 'password')
        assert user.email == 'test@example.com'
        assert user.id is not None

    def test_duplicate_email(self):
        """Test duplicate email handling"""
        self.db.create_user('test@example.com', 'pass1')
        with pytest.raises(DuplicateEmailError):
            self.db.create_user('test@example.com', 'pass2')

# Performance testing
@pytest.mark.benchmark
def test_performance(benchmark):
    """Benchmark function performance"""
    result = benchmark(expensive_operation, 1000)
    assert result is not None
```

### 14.2 Test-Driven Development (TDD)

```python
"""
TDD Example: Building a shopping cart

Step 1: Write failing test
Step 2: Write minimal code to pass
Step 3: Refactor
Step 4: Repeat
"""

# Test file: test_shopping_cart.py
import pytest

class TestShoppingCart:
    """TDD example for shopping cart"""

    def test_new_cart_is_empty(self):
        cart = ShoppingCart()
        assert cart.total() == 0
        assert len(cart.items) == 0

    def test_add_item_to_cart(self):
        cart = ShoppingCart()
        cart.add_item('Apple', 1.50, 2)
        assert len(cart.items) == 1
        assert cart.total() == 3.00

    def test_remove_item_from_cart(self):
        cart = ShoppingCart()
        cart.add_item('Apple', 1.50, 2)
        cart.remove_item('Apple')
        assert len(cart.items) == 0

    def test_apply_discount(self):
        cart = ShoppingCart()
        cart.add_item('Apple', 1.50, 10)
        cart.apply_discount(0.1)  # 10% discount
        assert cart.total() == 13.50

# Implementation: shopping_cart.py
class ShoppingCart:
    """Shopping cart implementation"""

    def __init__(self):
        self.items = []
        self.discount = 0

    def add_item(self, name: str, price: float, quantity: int):
        """Add item to cart"""
        self.items.append({
            'name': name,
            'price': price,
            'quantity': quantity
        })

    def remove_item(self, name: str):
        """Remove item from cart"""
        self.items = [item for item in self.items
                     if item['name'] != name]

    def apply_discount(self, discount: float):
        """Apply discount percentage"""
        self.discount = discount

    def total(self) -> float:
        """Calculate total price"""
        subtotal = sum(item['price'] * item['quantity']
                      for item in self.items)
        return subtotal * (1 - self.discount)
```

---

# PART 3: ALGORITHMS AND DATA STRUCTURES

## Module 15: Professional Algorithms

### 15.1 Sorting Algorithms

```python
from typing import List, TypeVar, Callable
import random

T = TypeVar('T')

def quick_sort(arr: List[T], key: Callable = None) -> List[T]:
    """
    Quick sort implementation - O(n log n) average
    Production-ready with custom key support
    """
    if len(arr) <= 1:
        return arr

    key_func = key or (lambda x: x)
    pivot = arr[len(arr) // 2]
    pivot_value = key_func(pivot)

    left = [x for x in arr if key_func(x) < pivot_value]
    middle = [x for x in arr if key_func(x) == pivot_value]
    right = [x for x in arr if key_func(x) > pivot_value]

    return quick_sort(left, key) + middle + quick_sort(right, key)

def merge_sort(arr: List[T]) -> List[T]:
    """
    Merge sort - O(n log n) guaranteed
    Stable sort, good for large datasets
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left: List[T], right: List[T]) -> List[T]:
    """Merge two sorted arrays"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def heap_sort(arr: List[T]) -> List[T]:
    """
    Heap sort - O(n log n)
    In-place sorting, memory efficient
    """
    def heapify(arr: List[T], n: int, i: int):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements from heap
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

    return arr
```

### 15.2 Search Algorithms

```python
from typing import List, Optional, TypeVar

T = TypeVar('T')

def binary_search(arr: List[T], target: T) -> Optional[int]:
    """
    Binary search - O(log n)
    Requires sorted array
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return None

def binary_search_leftmost(arr: List[T], target: T) -> int:
    """Find leftmost occurrence"""
    left, right = 0, len(arr)

    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left

def interpolation_search(arr: List[int], target: int) -> Optional[int]:
    """
    Interpolation search - O(log log n) for uniformly distributed data
    Better than binary search for certain datasets
    """
    low, high = 0, len(arr) - 1

    while low <= high and target >= arr[low] and target <= arr[high]:
        if low == high:
            if arr[low] == target:
                return low
            return None

        # Estimate position
        pos = low + int(((target - arr[low]) / (arr[high] - arr[low])) * (high - low))

        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return None
```

### 15.3 Advanced Data Structures

```python
from typing import Any, Optional, List
from collections import defaultdict
import heapq

class TrieNode:
    """Trie (Prefix Tree) implementation for autocomplete"""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word = None

class Trie:
    """
    Trie data structure for efficient string operations
    Use case: Autocomplete, spell checking, IP routing
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        """Insert word into trie - O(m) where m is word length"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.word = word

    def search(self, word: str) -> bool:
        """Search for exact word - O(m)"""
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> List[str]:
        """Find all words with given prefix"""
        node = self._find_node(prefix)
        if not node:
            return []

        results = []
        self._collect_words(node, results)
        return results

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """Find node corresponding to prefix"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect_words(self, node: TrieNode, results: List[str]):
        """Collect all words from node"""
        if node.is_end_of_word:
            results.append(node.word)

        for child in node.children.values():
            self._collect_words(child, results)

class Graph:
    """
    Graph implementation for network problems
    Use case: Social networks, routing, recommendations
    """
    def __init__(self, directed: bool = False):
        self.graph = defaultdict(list)
        self.directed = directed

    def add_edge(self, u: Any, v: Any, weight: float = 1):
        """Add edge to graph"""
        self.graph[u].append((v, weight))
        if not self.directed:
            self.graph[v].append((u, weight))

    def bfs(self, start: Any) -> List[Any]:
        """Breadth-first search"""
        visited = set()
        queue = [start]
        result = []

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                result.append(node)
                queue.extend([n for n, w in self.graph[node] if n not in visited])

        return result

    def dfs(self, start: Any, visited: Optional[set] = None) -> List[Any]:
        """Depth-first search"""
        if visited is None:
            visited = set()

        visited.add(start)
        result = [start]

        for neighbor, weight in self.graph[start]:
            if neighbor not in visited:
                result.extend(self.dfs(neighbor, visited))

        return result

    def dijkstra(self, start: Any) -> dict:
        """
        Dijkstra's shortest path algorithm
        Returns shortest distances from start to all nodes
        """
        distances = {node: float('infinity') for node in self.graph}
        distances[start] = 0
        pq = [(0, start)]

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            if current_dist > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node]:
                distance = current_dist + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances

class LRUCache:
    """
    LRU Cache implementation
    Use case: Caching, memory management
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.order = []

    def get(self, key: Any) -> Optional[Any]:
        """Get value and mark as recently used"""
        if key not in self.cache:
            return None

        # Move to end (most recent)
        self.order.remove(key)
        self.order.append(key)

        return self.cache[key]

    def put(self, key: Any, value: Any):
        """Put value and evict least recently used if needed"""
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            # Evict least recently used
            lru_key = self.order.pop(0)
            del self.cache[lru_key]

        self.cache[key] = value
        self.order.append(key)
```

---

# PART 4: DATABASE MASTERY

## Module 16: Professional Database Development

### 16.1 Advanced SQL with SQLAlchemy

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Index, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.pool import QueuePool
from datetime import datetime
from typing import List, Optional

Base = declarative_base()

# Professional model design
class User(Base):
    """User model with relationships and constraints"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')
    reviews = relationship('Review', back_populates='user')

    # Indexes
    __table_args__ = (
        Index('idx_email_username', 'email', 'username'),
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"

class Product(Base):
    """Product model"""
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    category = relationship('Category', back_populates='products')
    order_items = relationship('OrderItem', back_populates='product')
    reviews = relationship('Review', back_populates='product')

class Order(Base):
    """Order model"""
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship('User', back_populates='orders')
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

class OrderItem(Base):
    """Order items (many-to-many relationship table)"""
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # Relationships
    order = relationship('Order', back_populates='items')
    product = relationship('Product', back_populates='order_items')

# Professional database manager
class DatabaseManager:
    """Professional database connection and session management"""

    def __init__(self, database_url: str, pool_size: int = 10):
        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=pool_size,
            max_overflow=20,
            pool_pre_ping=True,  # Verify connections before using
            echo=False  # Set to True for SQL logging
        )
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Get new database session"""
        return self.Session()

    def execute_query(self, query: str, params: dict = None):
        """Execute raw SQL query"""
        with self.engine.connect() as conn:
            result = conn.execute(query, params or {})
            return result.fetchall()

# Professional repository pattern
class UserRepository:
    """Repository pattern for User operations"""

    def __init__(self, session):
        self.session = session

    def create(self, email: str, username: str, password_hash: str) -> User:
        """Create new user"""
        user = User(email=email, username=username, password_hash=password_hash)
        self.session.add(user)
        self.session.commit()
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.session.query(User).filter(User.email == email).first()

    def get_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        """Get all users with pagination"""
        return self.session.query(User).limit(limit).offset(offset).all()

    def update(self, user_id: int, **kwargs) -> Optional[User]:
        """Update user"""
        user = self.get_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            self.session.commit()
        return user

    def delete(self, user_id: int) -> bool:
        """Delete user"""
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def search(self, query: str) -> List[User]:
        """Search users by email or username"""
        return self.session.query(User).filter(
            (User.email.contains(query)) | (User.username.contains(query))
        ).all()
```

[CONTINUED IN NEXT FILE - THIS IS MASSIVE]
