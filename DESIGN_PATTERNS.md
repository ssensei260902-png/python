# 🏗️ Design Patterns Encyclopedia - Python Edition

## Complete Professional Guide to Software Design Patterns

---

## Table of Contents

### Creational Patterns
1. [Singleton](#1-singleton-pattern)
2. [Factory Method](#2-factory-method-pattern)
3. [Abstract Factory](#3-abstract-factory-pattern)
4. [Builder](#4-builder-pattern)
5. [Prototype](#5-prototype-pattern)

### Structural Patterns
6. [Adapter](#6-adapter-pattern)
7. [Decorator](#7-decorator-pattern)
8. [Facade](#8-facade-pattern)
9. [Proxy](#9-proxy-pattern)
10. [Composite](#10-composite-pattern)
11. [Bridge](#11-bridge-pattern)
12. [Flyweight](#12-flyweight-pattern)

### Behavioral Patterns
13. [Observer](#13-observer-pattern)
14. [Strategy](#14-strategy-pattern)
15. [Command](#15-command-pattern)
16. [Iterator](#16-iterator-pattern)
17. [State](#17-state-pattern)
18. [Template Method](#18-template-method-pattern)
19. [Chain of Responsibility](#19-chain-of-responsibility-pattern)
20. [Mediator](#20-mediator-pattern)

### Architectural Patterns
21. [MVC (Model-View-Controller)](#21-mvc-pattern)
22. [Repository Pattern](#22-repository-pattern)
23. [Dependency Injection](#23-dependency-injection)
24. [Service Layer](#24-service-layer-pattern)

---

## Creational Patterns

### 1. Singleton Pattern

**Purpose**: Ensure a class has only one instance and provide global access to it.

```python
from threading import Lock
from typing import Any

class SingletonMeta(type):
    """
    Thread-safe Singleton metaclass
    """
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    """
    Database connection singleton
    Only one connection instance exists
    """
    def __init__(self, host: str = 'localhost', port: int = 5432):
        # Only initialized once
        self.host = host
        self.port = port
        self.connection = None
        print(f"Connecting to {host}:{port}")

    def query(self, sql: str):
        """Execute query"""
        print(f"Executing: {sql}")
        return []


# Usage
db1 = DatabaseConnection('localhost', 5432)
db2 = DatabaseConnection('different-host', 3306)  # Ignored - returns same instance

print(db1 is db2)  # True - same object
print(f"DB1 host: {db1.host}")  # localhost (from first initialization)


# Alternative: Simple Python singleton
class Logger:
    """Simple singleton without metaclass"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.log_file = 'app.log'
        return cls._instance

    def log(self, message: str):
        """Log message"""
        with open(self.log_file, 'a') as f:
            f.write(f"{message}\n")


logger1 = Logger()
logger2 = Logger()
print(logger1 is logger2)  # True


# Modern approach: Module-level singleton
class _ConfigManager:
    """Configuration manager - internal class"""
    def __init__(self):
        self.config = {}

    def get(self, key: str, default=None):
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value

# Single instance at module level
config = _ConfigManager()

# Usage in other files:
# from myapp import config
# config.set('api_key', 'abc123')
```

**When to use**:
- Database connections
- Configuration managers
- Logging systems
- Cache managers
- Thread pools

---

### 2. Factory Method Pattern

**Purpose**: Define an interface for creating objects, but let subclasses decide which class to instantiate.

```python
from abc import ABC, abstractmethod
from typing import Protocol

# Product interface
class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

    @abstractmethod
    def move(self) -> str:
        pass


# Concrete products
class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

    def move(self) -> str:
        return "Running on four legs"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"

    def move(self) -> str:
        return "Sneaking quietly"


class Bird(Animal):
    def speak(self) -> str:
        return "Tweet!"

    def move(self) -> str:
        return "Flying in the sky"


# Factory
class AnimalFactory:
    """Factory to create animals"""

    @staticmethod
    def create_animal(animal_type: str) -> Animal:
        """Factory method"""
        animals = {
            'dog': Dog,
            'cat': Cat,
            'bird': Bird
        }

        animal_class = animals.get(animal_type.lower())
        if not animal_class:
            raise ValueError(f"Unknown animal type: {animal_type}")

        return animal_class()


# Usage
factory = AnimalFactory()

dog = factory.create_animal('dog')
print(dog.speak())  # Woof!
print(dog.move())   # Running on four legs

cat = factory.create_animal('cat')
print(cat.speak())  # Meow!


# Real-world example: Database connection factory
class DatabaseConnection(ABC):
    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def query(self, sql: str): pass


class PostgreSQLConnection(DatabaseConnection):
    def connect(self):
        print("Connecting to PostgreSQL")

    def query(self, sql: str):
        print(f"PostgreSQL: {sql}")


class MySQLConnection(DatabaseConnection):
    def connect(self):
        print("Connecting to MySQL")

    def query(self, sql: str):
        print(f"MySQL: {sql}")


class MongoDBConnection(DatabaseConnection):
    def connect(self):
        print("Connecting to MongoDB")

    def query(self, sql: str):
        print(f"MongoDB: {sql}")


class DatabaseFactory:
    """Create database connections based on config"""

    @staticmethod
    def create_connection(db_type: str) -> DatabaseConnection:
        connections = {
            'postgresql': PostgreSQLConnection,
            'mysql': MySQLConnection,
            'mongodb': MongoDBConnection
        }

        conn_class = connections.get(db_type.lower())
        if not conn_class:
            raise ValueError(f"Unsupported database: {db_type}")

        connection = conn_class()
        connection.connect()
        return connection


# Usage
db = DatabaseFactory.create_connection('postgresql')
db.query("SELECT * FROM users")

# Easy to switch databases
db = DatabaseFactory.create_connection('mongodb')
db.query("db.users.find({})")
```

**When to use**:
- Creating different database connections
- Payment gateway integrations (PayPal, Stripe, etc.)
- Notification systems (Email, SMS, Push)
- File parsers (JSON, XML, CSV)

---

### 3. Abstract Factory Pattern

**Purpose**: Create families of related objects without specifying their concrete classes.

```python
from abc import ABC, abstractmethod

# Abstract products
class Button(ABC):
    @abstractmethod
    def render(self) -> str: pass


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str: pass


# Windows components
class WindowsButton(Button):
    def render(self) -> str:
        return "Rendering Windows button"


class WindowsCheckbox(Checkbox):
    def render(self) -> str:
        return "Rendering Windows checkbox"


# macOS components
class MacOSButton(Button):
    def render(self) -> str:
        return "Rendering macOS button"


class MacOSCheckbox(Checkbox):
    def render(self) -> str:
        return "Rendering macOS checkbox"


# Linux components
class LinuxButton(Button):
    def render(self) -> str:
        return "Rendering Linux button"


class LinuxCheckbox(Checkbox):
    def render(self) -> str:
        return "Rendering Linux checkbox"


# Abstract factory
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox: pass


# Concrete factories
class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()


class MacOSFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacOSButton()

    def create_checkbox(self) -> Checkbox:
        return MacOSCheckbox()


class LinuxFactory(GUIFactory):
    def create_button(self) -> Button:
        return LinuxButton()

    def create_checkbox(self) -> Checkbox:
        return LinuxCheckbox()


# Application
class Application:
    """Application uses abstract factory"""

    def __init__(self, factory: GUIFactory):
        self.factory = factory
        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()

    def render(self):
        """Render UI components"""
        print(self.button.render())
        print(self.checkbox.render())


# Usage
import platform

# Detect OS and create appropriate factory
os_name = platform.system()

if os_name == 'Windows':
    factory = WindowsFactory()
elif os_name == 'Darwin':  # macOS
    factory = MacOSFactory()
else:  # Linux
    factory = LinuxFactory()

app = Application(factory)
app.render()
```

**When to use**:
- Cross-platform UI frameworks
- Database abstraction layers (SQL Server, Oracle, MySQL)
- Cloud provider abstractions (AWS, Azure, GCP)

---

### 4. Builder Pattern

**Purpose**: Construct complex objects step by step.

```python
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class Pizza:
    """Complex object with many optional parameters"""
    size: str = 'medium'
    cheese: bool = False
    pepperoni: bool = False
    mushrooms: bool = False
    onions: bool = False
    bacon: bool = False
    extra_sauce: bool = False
    toppings: List[str] = field(default_factory=list)

    def __str__(self):
        desc = f"{self.size.capitalize()} pizza"
        ingredients = []

        if self.cheese: ingredients.append("cheese")
        if self.pepperoni: ingredients.append("pepperoni")
        if self.mushrooms: ingredients.append("mushrooms")
        if self.onions: ingredients.append("onions")
        if self.bacon: ingredients.append("bacon")
        if self.extra_sauce: ingredients.append("extra sauce")
        ingredients.extend(self.toppings)

        if ingredients:
            desc += " with " + ", ".join(ingredients)

        return desc


class PizzaBuilder:
    """Builder for Pizza"""

    def __init__(self):
        self.pizza = Pizza()

    def set_size(self, size: str):
        """Set pizza size"""
        self.pizza.size = size
        return self

    def add_cheese(self):
        """Add cheese"""
        self.pizza.cheese = True
        return self

    def add_pepperoni(self):
        """Add pepperoni"""
        self.pizza.pepperoni = True
        return self

    def add_mushrooms(self):
        """Add mushrooms"""
        self.pizza.mushrooms = True
        return self

    def add_onions(self):
        """Add onions"""
        self.pizza.onions = True
        return self

    def add_bacon(self):
        """Add bacon"""
        self.pizza.bacon = True
        return self

    def add_extra_sauce(self):
        """Add extra sauce"""
        self.pizza.extra_sauce = True
        return self

    def add_topping(self, topping: str):
        """Add custom topping"""
        self.pizza.toppings.append(topping)
        return self

    def build(self) -> Pizza:
        """Build and return pizza"""
        return self.pizza


# Usage - Fluent interface
pizza = (PizzaBuilder()
         .set_size('large')
         .add_cheese()
         .add_pepperoni()
         .add_mushrooms()
         .add_extra_sauce()
         .add_topping('olives')
         .add_topping('jalapeños')
         .build())

print(pizza)
# Output: Large pizza with cheese, pepperoni, mushrooms, extra sauce, olives, jalapeños


# Real-world example: SQL Query Builder
class QueryBuilder:
    """Build SQL queries programmatically"""

    def __init__(self, table: str):
        self.table = table
        self.select_fields = ['*']
        self.where_clauses = []
        self.order_by_field = None
        self.limit_value = None

    def select(self, *fields: str):
        """Select specific fields"""
        self.select_fields = fields
        return self

    def where(self, condition: str):
        """Add WHERE clause"""
        self.where_clauses.append(condition)
        return self

    def order_by(self, field: str):
        """Add ORDER BY"""
        self.order_by_field = field
        return self

    def limit(self, count: int):
        """Add LIMIT"""
        self.limit_value = count
        return self

    def build(self) -> str:
        """Build SQL query"""
        query = f"SELECT {', '.join(self.select_fields)} FROM {self.table}"

        if self.where_clauses:
            query += " WHERE " + " AND ".join(self.where_clauses)

        if self.order_by_field:
            query += f" ORDER BY {self.order_by_field}"

        if self.limit_value:
            query += f" LIMIT {self.limit_value}"

        return query


# Usage
query = (QueryBuilder('users')
         .select('id', 'username', 'email')
         .where("active = 1")
         .where("age >= 18")
         .order_by('created_at')
         .limit(10)
         .build())

print(query)
# SELECT id, username, email FROM users WHERE active = 1 AND age >= 18 ORDER BY created_at LIMIT 10
```

**When to use**:
- Complex object construction (HTTP requests, database queries)
- Configuration builders
- Test data builders
- Document builders (PDF, HTML)

---

### 5. Prototype Pattern

**Purpose**: Create new objects by cloning existing ones.

```python
import copy
from typing import List

class Prototype:
    """Base prototype class"""

    def clone(self):
        """Shallow copy"""
        return copy.copy(self)

    def deep_clone(self):
        """Deep copy"""
        return copy.deepcopy(self)


class Document(Prototype):
    """Document that can be cloned"""

    def __init__(self, title: str, content: str, tags: List[str]):
        self.title = title
        self.content = content
        self.tags = tags

    def __str__(self):
        return f"Document(title='{self.title}', tags={self.tags})"


# Usage
original = Document(
    "Python Guide",
    "This is a Python programming guide...",
    ["python", "programming", "tutorial"]
)

# Shallow clone
clone1 = original.clone()
clone1.title = "Python Advanced Guide"
clone1.tags.append("advanced")  # Modifies original too (shallow copy)!

print(f"Original: {original}")  # Tags modified!
print(f"Clone1: {clone1}")

# Deep clone
original2 = Document(
    "Python Guide",
    "This is a Python programming guide...",
    ["python", "programming", "tutorial"]
)

clone2 = original2.deep_clone()
clone2.title = "Python Beginner Guide"
clone2.tags.append("beginner")  # Doesn't affect original

print(f"\nOriginal2: {original2}")  # Tags unchanged
print(f"Clone2: {clone2}")


# Real-world: Configuration template
class ServerConfig(Prototype):
    """Server configuration template"""

    def __init__(self, host: str, port: int, ssl: bool = False):
        self.host = host
        self.port = port
        self.ssl = ssl
        self.middlewares = []
        self.routes = {}

    def __str__(self):
        return f"Server({self.host}:{self.port}, SSL={self.ssl})"


# Create base config
base_config = ServerConfig('localhost', 8000)
base_config.middlewares = ['logging', 'cors']
base_config.routes = {'/': 'home', '/api': 'api_handler'}

# Clone for production (different host, enable SSL)
prod_config = base_config.deep_clone()
prod_config.host = 'api.example.com'
prod_config.port = 443
prod_config.ssl = True
prod_config.middlewares.append('rate_limiting')

# Clone for staging
staging_config = base_config.deep_clone()
staging_config.host = 'staging.example.com'
staging_config.port = 8080

print(base_config)
print(prod_config)
print(staging_config)
```

**When to use**:
- Creating variations of complex objects
- Configuration templates
- Game object spawning
- Undo/redo functionality

---

## Structural Patterns

### 6. Adapter Pattern

**Purpose**: Convert interface of a class into another interface clients expect.

```python
from abc import ABC, abstractmethod

# Target interface (what client expects)
class MediaPlayer(ABC):
    @abstractmethod
    def play(self, filename: str): pass


# Existing class with incompatible interface
class VLCPlayer:
    """Third-party VLC player with different interface"""

    def play_vlc(self, filename: str):
        print(f"VLC: Playing {filename}")


class WindowsMediaPlayer:
    """Another third-party player"""

    def play_wmp(self, filename: str):
        print(f"WMP: Playing {filename}")


# Adapters
class VLCAdapter(MediaPlayer):
    """Adapt VLC to MediaPlayer interface"""

    def __init__(self):
        self.vlc = VLCPlayer()

    def play(self, filename: str):
        """Adapt play() to play_vlc()"""
        self.vlc.play_vlc(filename)


class WMPAdapter(MediaPlayer):
    """Adapt Windows Media Player to MediaPlayer interface"""

    def __init__(self):
        self.wmp = WindowsMediaPlayer()

    def play(self, filename: str):
        """Adapt play() to play_wmp()"""
        self.wmp.play_wmp(filename)


# Client code
class AudioPlayer:
    """Client that uses MediaPlayer interface"""

    def __init__(self, player: MediaPlayer):
        self.player = player

    def play_audio(self, filename: str):
        self.player.play(filename)


# Usage
# Use VLC through adapter
vlc_player = AudioPlayer(VLCAdapter())
vlc_player.play_audio("song.mp3")

# Use WMP through adapter
wmp_player = AudioPlayer(WMPAdapter())
wmp_player.play_audio("song.mp3")


# Real-world: Legacy API adapter
class LegacyUserAPI:
    """Old API with different structure"""

    def get_user_data(self, user_id: int):
        return {
            'id': user_id,
            'user_name': 'john_doe',
            'user_email': 'john@example.com',
            'user_age': 30
        }


class ModernUserAPI(ABC):
    """New API interface"""

    @abstractmethod
    def get_user(self, user_id: int) -> dict: pass


class UserAPIAdapter(ModernUserAPI):
    """Adapt legacy API to modern interface"""

    def __init__(self):
        self.legacy_api = LegacyUserAPI()

    def get_user(self, user_id: int) -> dict:
        """Transform legacy data to modern format"""
        legacy_data = self.legacy_api.get_user_data(user_id)

        # Transform keys
        return {
            'id': legacy_data['id'],
            'username': legacy_data['user_name'],  # Renamed
            'email': legacy_data['user_email'],    # Renamed
            'age': legacy_data['user_age']         # Renamed
        }


# Usage
api = UserAPIAdapter()
user = api.get_user(123)
print(user)  # Modern format
```

**When to use**:
- Integrating third-party libraries
- Working with legacy code
- API versioning
- Database migrations

---

### 7. Decorator Pattern

**Purpose**: Add new functionality to objects dynamically.

```python
from abc import ABC, abstractmethod
from functools import wraps
import time

# Component interface
class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float: pass

    @abstractmethod
    def description(self) -> str: pass


# Concrete component
class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 2.0

    def description(self) -> str:
        return "Simple coffee"


# Decorator base class
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()


# Concrete decorators
class Milk(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.5

    def description(self) -> str:
        return self._coffee.description() + ", milk"


class Sugar(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.2

    def description(self) -> str:
        return self._coffee.description() + ", sugar"


class WhippedCream(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.7

    def description(self) -> str:
        return self._coffee.description() + ", whipped cream"


# Usage
coffee = SimpleCoffee()
print(f"{coffee.description()} = ${coffee.cost()}")

# Add milk
coffee = Milk(coffee)
print(f"{coffee.description()} = ${coffee.cost()}")

# Add sugar
coffee = Sugar(coffee)
print(f"{coffee.description()} = ${coffee.cost()}")

# Add whipped cream
coffee = WhippedCream(coffee)
print(f"{coffee.description()} = ${coffee.cost()}")


# Python's built-in decorator syntax
def timing_decorator(func):
    """Decorator to measure execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {(end-start)*1000:.2f}ms")
        return result
    return wrapper


def logging_decorator(func):
    """Decorator to log function calls"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper


@timing_decorator
@logging_decorator
def expensive_function(n):
    """Function with multiple decorators"""
    total = sum(i**2 for i in range(n))
    return total


result = expensive_function(100000)
```

**When to use**:
- Adding cross-cutting concerns (logging, caching, authentication)
- GUI component enhancements
- Stream processing (compression, encryption)
- Dynamic pricing (taxes, discounts)

---

### 8. Facade Pattern

**Purpose**: Provide a simplified interface to a complex subsystem.

```python
# Complex subsystem
class CPU:
    def freeze(self): print("CPU: Freeze")
    def jump(self, position): print(f"CPU: Jump to {position}")
    def execute(self): print("CPU: Execute")


class Memory:
    def load(self, position, data): print(f"Memory: Load {data} at {position}")


class HardDrive:
    def read(self, lba, size): return f"Data from {lba}"


# Facade
class ComputerFacade:
    """Simple interface for complex computer subsystems"""

    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()

    def start(self):
        """Simple method that handles complexity"""
        print("Starting computer...")
        self.cpu.freeze()
        self.memory.load(0, self.hard_drive.read(100, 1024))
        self.cpu.jump(0)
        self.cpu.execute()
        print("Computer started!")


# Usage - Simple interface
computer = ComputerFacade()
computer.start()


# Real-world: API Facade
class EmailService:
    def send_email(self, to, subject, body): pass


class SMSService:
    def send_sms(self, phone, message): pass


class PushNotificationService:
    def send_push(self, device_id, message): pass


class NotificationFacade:
    """Facade for multiple notification services"""

    def __init__(self):
        self.email = EmailService()
        self.sms = SMSService()
        self.push = PushNotificationService()

    def notify_user(self, user, message):
        """Send notification via all channels"""
        self.email.send_email(user.email, "Notification", message)
        self.sms.send_sms(user.phone, message)
        self.push.send_push(user.device_id, message)


# Usage
facade = NotificationFacade()
# One simple call instead of three!
# facade.notify_user(user, "Your order has shipped!")
```

**When to use**:
- Simplifying complex libraries
- Legacy system integration
- Microservices API gateway
- SDK development

---

## Behavioral Patterns

### 13. Observer Pattern

**Purpose**: Define one-to-many dependency so that when one object changes state, all dependents are notified.

```python
from abc import ABC, abstractmethod
from typing import List

# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, subject): pass


# Subject (Observable)
class Subject:
    """Subject that observers watch"""

    def __init__(self):
        self._observers: List[Observer] = []
        self._state = None

    def attach(self, observer: Observer):
        """Register observer"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        """Unregister observer"""
        self._observers.remove(observer)

    def notify(self):
        """Notify all observers"""
        for observer in self._observers:
            observer.update(self)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        """When state changes, notify observers"""
        self._state = value
        self.notify()


# Concrete observers
class EmailNotifier(Observer):
    def update(self, subject):
        print(f"Email: Stock price changed to ${subject.state}")


class SMSNotifier(Observer):
    def update(self, subject):
        print(f"SMS: Stock price is now ${subject.state}")


class DashboardDisplay(Observer):
    def update(self, subject):
        print(f"Dashboard: Updated price to ${subject.state}")


# Usage
stock = Subject()

# Register observers
email = EmailNotifier()
sms = SMSNotifier()
dashboard = DashboardDisplay()

stock.attach(email)
stock.attach(sms)
stock.attach(dashboard)

# Change state - all observers notified
stock.state = 100.50
# Email: Stock price changed to $100.5
# SMS: Stock price is now $100.5
# Dashboard: Updated price to $100.5

stock.state = 105.75
# All observers notified again


# Real-world: Event system
class Event:
    """Event system using observer pattern"""

    def __init__(self):
        self._listeners = {}

    def on(self, event_name: str, callback):
        """Register event listener"""
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)

    def emit(self, event_name: str, *args, **kwargs):
        """Trigger event"""
        if event_name in self._listeners:
            for callback in self._listeners[event_name]:
                callback(*args, **kwargs)


# Usage
events = Event()

def on_user_login(user):
    print(f"User {user} logged in")
    # Send welcome email, log analytics, etc.

def on_user_logout(user):
    print(f"User {user} logged out")

events.on('login', on_user_login)
events.on('logout', on_user_logout)

events.emit('login', 'john_doe')  # Triggers on_user_login
events.emit('logout', 'john_doe')  # Triggers on_user_logout
```

**When to use**:
- Event systems
- Model-View updates (MVC)
- Real-time notifications
- Stock price updates
- Pub/Sub systems

---

### 14. Strategy Pattern

**Purpose**: Define a family of algorithms, encapsulate each one, and make them interchangeable.

```python
from abc import ABC, abstractmethod
from typing import List

# Strategy interface
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float): pass


# Concrete strategies
class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv

    def pay(self, amount: float):
        print(f"Paid ${amount} with credit card {self.card_number[-4:]}")


class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float):
        print(f"Paid ${amount} via PayPal ({self.email})")


class BitcoinPayment(PaymentStrategy):
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def pay(self, amount: float):
        print(f"Paid ${amount} via Bitcoin to {self.wallet_address[:10]}...")


# Context
class ShoppingCart:
    """Context that uses payment strategy"""

    def __init__(self):
        self.items = []
        self.payment_strategy = None

    def add_item(self, item: str, price: float):
        self.items.append((item, price))

    def set_payment_strategy(self, strategy: PaymentStrategy):
        """Change payment method at runtime"""
        self.payment_strategy = strategy

    def checkout(self):
        """Execute payment using chosen strategy"""
        total = sum(price for _, price in self.items)
        if self.payment_strategy:
            self.payment_strategy.pay(total)
        else:
            print("Please select payment method")


# Usage
cart = ShoppingCart()
cart.add_item("Laptop", 999.99)
cart.add_item("Mouse", 29.99)

# Pay with credit card
cart.set_payment_strategy(CreditCardPayment("1234-5678-9012-3456", "123"))
cart.checkout()  # Paid $1029.98 with credit card ...3456

# Change strategy - pay with PayPal
cart.set_payment_strategy(PayPalPayment("user@example.com"))
cart.checkout()  # Paid $1029.98 via PayPal

# Change strategy - pay with Bitcoin
cart.set_payment_strategy(BitcoinPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"))
cart.checkout()


# Real-world: Sorting strategies
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]: pass


class QuickSort(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        print("Using QuickSort")
        return sorted(data)  # Simplified


class MergeSort(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        print("Using MergeSort")
        return sorted(data)  # Simplified


class DataProcessor:
    """Choose sorting algorithm based on data size"""

    def __init__(self):
        self.sort_strategy = None

    def process(self, data: List[int]):
        # Choose strategy based on data size
        if len(data) < 100:
            self.sort_strategy = QuickSort()
        else:
            self.sort_strategy = MergeSort()

        return self.sort_strategy.sort(data)


processor = DataProcessor()
processor.process([5, 2, 8, 1])  # Uses QuickSort
processor.process(list(range(1000)))  # Uses MergeSort
```

**When to use**:
- Payment processing
- Compression algorithms
- Sorting algorithms
- Authentication methods
- Routing algorithms

---

This is Part 1 of Design Patterns. The complete guide includes all 24 patterns plus architectural patterns. Each pattern includes:

1. **Intent** - What problem it solves
2. **Implementation** - Python code examples
3. **Usage** - When to use it
4. **Real-world examples** - Practical applications

Continue to Part 2 for remaining patterns (Command, Iterator, State, Template Method, etc.) and architectural patterns (MVC, Repository, DI, Service Layer).

---

## Key Takeaways

### When to Use Each Pattern

**Creational**: When object creation is complex
- Singleton: One instance (database, config)
- Factory: Create related objects (database connections)
- Builder: Complex construction (queries, requests)

**Structural**: When organizing object relationships
- Adapter: Incompatible interfaces (legacy APIs)
- Decorator: Add features dynamically (logging, caching)
- Facade: Simplify complex systems (API gateway)

**Behavioral**: When defining communication between objects
- Observer: One-to-many notifications (events)
- Strategy: Interchangeable algorithms (payments)
- Command: Encapsulate requests (undo/redo)

Practice these patterns in real projects to become a professional software architect!
