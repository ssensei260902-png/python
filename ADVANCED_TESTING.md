# 🧪 Advanced Testing Strategies in Python

## Complete Professional Testing Guide from Unit to E2E

---

## Table of Contents

1. [Unit Testing with pytest](#1-unit-testing-with-pytest)
2. [Test-Driven Development (TDD)](#2-test-driven-development)
3. [Mocking and Patching](#3-mocking-and-patching)
4. [Integration Testing](#4-integration-testing)
5. [End-to-End Testing](#5-end-to-end-testing)
6. [Performance Testing](#6-performance-testing)
7. [Property-Based Testing](#7-property-based-testing)
8. [Testing Best Practices](#8-testing-best-practices)

---

## 1. Unit Testing with pytest

### 1.1 pytest Fundamentals

```python
# test_calculator.py
import pytest

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


# Test fixture
@pytest.fixture
def calculator():
    """Fixture to create calculator instance"""
    return Calculator()


# Basic tests
def test_add(calculator):
    assert calculator.add(2, 3) == 5
    assert calculator.add(-1, 1) == 0


def test_subtract(calculator):
    assert calculator.subtract(5, 3) == 2
    assert calculator.subtract(0, 5) == -5


def test_multiply(calculator):
    assert calculator.multiply(3, 4) == 12
    assert calculator.multiply(-2, 3) == -6


def test_divide(calculator):
    assert calculator.divide(6, 2) == 3
    assert calculator.divide(5, 2) == 2.5


def test_divide_by_zero(calculator):
    """Test exception handling"""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculator.divide(5, 0)


# Parametrized tests
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add_parametrized(calculator, a, b, expected):
    assert calculator.add(a, b) == expected


# Test markers
@pytest.mark.slow
def test_slow_operation(calculator):
    """Mark slow tests"""
    import time
    time.sleep(2)
    assert True


@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass


@pytest.mark.xfail(reason="Known bug")
def test_known_issue():
    assert False


# Run tests:
# pytest test_calculator.py -v
# pytest -m "not slow"  # Skip slow tests
# pytest --cov=calculator --cov-report=html  # Coverage report
```

### 1.2 Advanced Fixtures

```python
# conftest.py - shared fixtures
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import User

@pytest.fixture(scope="session")
def engine():
    """Create test database engine"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(engine):
    """Create new database session for each test"""
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.rollback()
    session.close()


@pytest.fixture
def sample_user(db_session):
    """Create sample user"""
    user = User(username="testuser", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user


# test_database.py
def test_create_user(db_session):
    """Test user creation"""
    user = User(username="john", email="john@example.com")
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.username == "john"


def test_user_relationship(db_session, sample_user):
    """Test with sample user fixture"""
    assert sample_user.id is not None
    assert sample_user.username == "testuser"
```

---

## 2. Test-Driven Development (TDD)

### 2.1 TDD Cycle: Red → Green → Refactor

```python
# Example: Implementing a Stack with TDD

# Step 1: Write failing test (RED)
import pytest

class TestStack:
    def test_stack_is_empty_when_created(self):
        stack = Stack()
        assert stack.is_empty() == True

    def test_stack_size_increases_when_pushed(self):
        stack = Stack()
        stack.push(1)
        assert stack.size() == 1

    def test_stack_pop_returns_last_item(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        assert stack.pop() == 2
        assert stack.size() == 1

    def test_stack_pop_empty_raises_error(self):
        stack = Stack()
        with pytest.raises(IndexError):
            stack.pop()


# Step 2: Write minimal code to pass (GREEN)
class Stack:
    def __init__(self):
        self._items = []

    def is_empty(self):
        return len(self._items) == 0

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Cannot pop from empty stack")
        return self._items.pop()

    def size(self):
        return len(self._items)


# Step 3: Refactor (clean up code while keeping tests green)
class Stack:
    """Optimized stack implementation"""

    def __init__(self):
        self._items = []

    def is_empty(self) -> bool:
        return not self._items

    def push(self, item) -> None:
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("Cannot pop from empty stack")
        return self._items.pop()

    def peek(self):
        """View top item without removing"""
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items[-1]

    def size(self) -> int:
        return len(self._items)
```

---

## 3. Mocking and Patching

### 3.1 unittest.mock

```python
from unittest.mock import Mock, patch, MagicMock
import requests

# Code to test
class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.weather.com"

    def get_temperature(self, city):
        """Get temperature for city"""
        url = f"{self.base_url}/weather?city={city}&key={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['temperature']

    def send_alert(self, message):
        """Send email alert"""
        # Complex email sending logic
        pass


# Test with mocking
def test_get_temperature_success():
    """Mock HTTP request"""
    service = WeatherService("fake-api-key")

    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = {'temperature': 25}
    mock_response.status_code = 200

    # Patch requests.get
    with patch('requests.get', return_value=mock_response):
        temperature = service.get_temperature("London")
        assert temperature == 25


def test_get_temperature_api_error():
    """Test API error handling"""
    service = WeatherService("fake-api-key")

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("API Error")

    with patch('requests.get', return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            service.get_temperature("London")


# Mock methods
def test_send_alert():
    """Mock method call"""
    service = WeatherService("fake-api-key")

    with patch.object(service, 'send_alert') as mock_alert:
        service.send_alert("Temperature alert!")
        mock_alert.assert_called_once_with("Temperature alert!")


# Mock class
@patch('app.services.EmailService')
def test_with_mocked_class(MockEmailService):
    """Mock entire class"""
    mock_email = MockEmailService.return_value
    mock_email.send.return_value = True

    # Use mocked service
    result = mock_email.send("test@example.com", "Hello")
    assert result == True
    mock_email.send.assert_called_once()
```

### 3.2 pytest-mock

```python
# Using pytest-mock (cleaner syntax)
import pytest

def test_weather_service(mocker):
    """Test with pytest-mock"""
    # Mock requests.get
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.json.return_value = {'temperature': 30}

    service = WeatherService("api-key")
    temp = service.get_temperature("Paris")

    assert temp == 30
    mock_get.assert_called_once()


def test_spy_on_method(mocker):
    """Spy on method (calls real method but tracks calls)"""
    service = WeatherService("api-key")
    spy = mocker.spy(service, 'send_alert')

    service.send_alert("Alert!")

    spy.assert_called_once_with("Alert!")
```

---

## 4. Integration Testing

### 4.1 Testing Flask API

```python
import pytest
from flask import Flask
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    """Create Flask app for testing"""
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Get authentication headers"""
    # Login and get token
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'password'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_create_user(client):
    """Test user registration"""
    response = client.post('/api/users', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123'
    })

    assert response.status_code == 201
    assert response.json['username'] == 'newuser'


def test_get_user(client, auth_headers):
    """Test get user (authenticated)"""
    response = client.get('/api/users/1', headers=auth_headers)

    assert response.status_code == 200
    assert 'username' in response.json


def test_unauthorized_access(client):
    """Test endpoint requires authentication"""
    response = client.get('/api/users/1')
    assert response.status_code == 401
```

### 4.2 Testing with Database

```python
import pytest
from app.repositories import UserRepository
from app.models import User

@pytest.fixture
def user_repo(db_session):
    """User repository fixture"""
    return UserRepository(db_session)


def test_create_user_integration(user_repo):
    """Integration test for user creation"""
    user = user_repo.create(
        username='john',
        email='john@example.com',
        password='secret'
    )

    assert user.id is not None
    assert user_repo.count() == 1


def test_find_user_by_email(user_repo):
    """Test querying user"""
    user_repo.create(
        username='jane',
        email='jane@example.com',
        password='secret'
    )

    found = user_repo.find_by_email('jane@example.com')

    assert found is not None
    assert found.username == 'jane'


def test_update_user(user_repo):
    """Test updating user"""
    user = user_repo.create(
        username='bob',
        email='bob@example.com',
        password='secret'
    )

    user_repo.update(user.id, username='bobby')
    updated = user_repo.find_by_id(user.id)

    assert updated.username == 'bobby'
```

---

## 5. End-to-End Testing

### 5.1 Selenium WebDriver

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

@pytest.fixture
def driver():
    """Create Chrome driver"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run without GUI
    driver = webdriver.Chrome(options=options)

    yield driver

    driver.quit()


def test_login_page(driver):
    """Test login functionality"""
    driver.get("http://localhost:5000/login")

    # Find elements
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-btn")

    # Fill form
    username_input.send_keys("testuser")
    password_input.send_keys("password123")
    login_button.click()

    # Wait for redirect
    WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard")
    )

    assert "Dashboard" in driver.title


def test_create_post_flow(driver):
    """Test complete post creation flow"""
    # Login first
    driver.get("http://localhost:5000/login")
    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "login-btn").click()

    # Wait for dashboard
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "create-post-btn"))
    )

    # Click create post
    driver.find_element(By.ID, "create-post-btn").click()

    # Fill post form
    driver.find_element(By.ID, "post-title").send_keys("Test Post")
    driver.find_element(By.ID, "post-content").send_keys("This is a test")
    driver.find_element(By.ID, "submit-post-btn").click()

    # Verify post created
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "post-item"))
    )

    posts = driver.find_elements(By.CLASS_NAME, "post-item")
    assert len(posts) > 0
    assert "Test Post" in driver.page_source
```

---

## 6. Performance Testing

### 6.1 Load Testing with Locust

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    """Simulate user behavior for load testing"""

    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks

    def on_start(self):
        """Login before starting tasks"""
        self.client.post("/api/login", json={
            "username": "testuser",
            "password": "password"
        })

    @task(3)  # Weight: run 3x more often
    def view_posts(self):
        """View posts list"""
        self.client.get("/api/posts")

    @task(2)
    def view_post_detail(self):
        """View single post"""
        post_id = 1  # In real test, randomize
        self.client.get(f"/api/posts/{post_id}")

    @task(1)
    def create_post(self):
        """Create new post"""
        self.client.post("/api/posts", json={
            "title": "Load Test Post",
            "content": "Testing under load"
        })

    @task(1)
    def search(self):
        """Search posts"""
        self.client.get("/api/posts/search?q=python")

# Run: locust -f load_test.py --host=http://localhost:8000
# Open browser: http://localhost:8089
```

### 6.2 Benchmarking with pytest-benchmark

```python
import pytest

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def fibonacci_optimized(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_optimized(n-1, memo) + fibonacci_optimized(n-2, memo)
    return memo[n]

def test_fibonacci_performance(benchmark):
    """Benchmark fibonacci function"""
    result = benchmark(fibonacci, 20)
    assert result == 6765

def test_fibonacci_optimized_performance(benchmark):
    """Benchmark optimized version"""
    result = benchmark(fibonacci_optimized, 20)
    assert result == 6765

# Run: pytest test_performance.py --benchmark-compare
```

---

## 7. Property-Based Testing

### 7.1 Hypothesis

```python
from hypothesis import given, strategies as st
import pytest

# Property-based testing with Hypothesis
@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """Addition is commutative: a + b = b + a"""
    assert a + b == b + a

@given(st.lists(st.integers()))
def test_reverse_twice_is_identity(lst):
    """Reversing twice returns original list"""
    assert list(reversed(list(reversed(lst)))) == lst

@given(st.text())
def test_string_strip_idempotent(s):
    """Stripping twice is same as stripping once"""
    assert s.strip().strip() == s.strip()

@given(st.lists(st.integers(), min_size=1))
def test_sorted_list_properties(lst):
    """Test sorted list properties"""
    sorted_lst = sorted(lst)

    # Same length
    assert len(sorted_lst) == len(lst)

    # All elements present
    assert set(sorted_lst) == set(lst)

    # Actually sorted
    for i in range(len(sorted_lst) - 1):
        assert sorted_lst[i] <= sorted_lst[i + 1]
```

---

## 8. Testing Best Practices

### 8.1 Test Organization

```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── test_api.py
│   ├── test_database.py
│   └── test_repositories.py
├── e2e/
│   └── test_user_flows.py
├── performance/
│   └── load_test.py
├── conftest.py
└── __init__.py
```

### 8.2 Testing Principles

```python
# 1. AAA Pattern: Arrange, Act, Assert
def test_user_creation():
    # Arrange
    username = "testuser"
    email = "test@example.com"

    # Act
    user = User(username=username, email=email)

    # Assert
    assert user.username == username
    assert user.email == email


# 2. One assertion per test (when possible)
def test_user_has_username():
    user = User(username="john", email="john@example.com")
    assert user.username == "john"

def test_user_has_email():
    user = User(username="john", email="john@example.com")
    assert user.email == "john@example.com"


# 3. Test edge cases
@pytest.mark.parametrize("input,expected", [
    ("", 0),           # Empty string
    ("a", 1),          # Single character
    ("hello", 5),      # Normal case
    ("  spaces  ", 9), # With spaces
    ("🎉", 1),         # Unicode
])
def test_string_length_edge_cases(input, expected):
    assert len(input) == expected


# 4. Use descriptive test names
def test_user_cannot_register_with_duplicate_email():
    """Test name explains what and why"""
    pass

# Not: test_user_1()
```

---

**Remember:** Good tests are **Fast, Independent, Repeatable, Self-Validating, and Timely (FIRST)**!

Practice TDD, aim for 80%+ code coverage, and always test edge cases!
