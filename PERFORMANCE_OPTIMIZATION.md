# ⚡ Python Performance Optimization & Profiling

## Complete Professional Guide to High-Performance Python

---

## Table of Contents

1. [Profiling & Benchmarking](#profiling--benchmarking)
2. [Memory Optimization](#memory-optimization)
3. [Algorithm Optimization](#algorithm-optimization)
4. [Caching Strategies](#caching-strategies)
5. [Database Optimization](#database-optimization)
6. [Async Programming](#async-programming)
7. [Parallel Processing](#parallel-processing)
8. [NumPy & Pandas Optimization](#numpy--pandas-optimization)
9. [Python Performance Tips](#python-performance-tips)
10. [Production Performance Monitoring](#production-performance-monitoring)

---

## 1. Profiling & Benchmarking

### 1.1 cProfile - CPU Profiling

```python
import cProfile
import pstats
from pstats import SortKey
from functools import wraps
import time

class Profiler:
    """Professional CPU profiling"""

    @staticmethod
    def profile_function(func):
        """Decorator to profile a function"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            profiler.enable()

            result = func(*args, **kwargs)

            profiler.disable()
            stats = pstats.Stats(profiler)
            stats.sort_stats(SortKey.CUMULATIVE)
            stats.print_stats(20)  # Top 20 functions

            return result
        return wrapper

    @staticmethod
    def profile_code(code_string: str, globals_dict: dict = None):
        """Profile code snippet"""
        profiler = cProfile.Profile()
        profiler.enable()

        exec(code_string, globals_dict or {})

        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats(SortKey.CUMULATIVE)
        stats.print_stats()

    @staticmethod
    def profile_to_file(func, output_file: str = 'profile.stats'):
        """Profile and save to file for analysis"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            profiler.enable()

            result = func(*args, **kwargs)

            profiler.disable()
            profiler.dump_stats(output_file)
            print(f"Profile saved to {output_file}")

            # View with: python -m pstats profile.stats
            return result
        return wrapper

# Usage
@Profiler.profile_function
def slow_function():
    """Example function to profile"""
    total = 0
    for i in range(1000000):
        total += i
    return total

result = slow_function()

# Profile specific code
Profiler.profile_code("""
data = [i**2 for i in range(100000)]
sum(data)
""")
```

### 1.2 line_profiler - Line-by-Line Profiling

```python
# Install: pip install line_profiler

# Method 1: Using decorator
from line_profiler import LineProfiler

def profile_lines(func):
    """Line-by-line profiling decorator"""
    def wrapper(*args, **kwargs):
        profiler = LineProfiler()
        profiler.add_function(func)
        profiler.enable()

        result = func(*args, **kwargs)

        profiler.disable()
        profiler.print_stats()

        return result
    return wrapper

@profile_lines
def process_data(data):
    """Process data - see which lines are slow"""
    result = []
    for item in data:                    # Line timing
        processed = item ** 2            # Line timing
        if processed > 100:              # Line timing
            result.append(processed)     # Line timing
    return result

# Method 2: Command line
# kernprof -l -v script.py

# Add @profile decorator to functions (no import needed)
# @profile
# def my_function():
#     pass
```

### 1.3 timeit - Accurate Benchmarking

```python
import timeit
from typing import Callable
import statistics

class Benchmark:
    """Professional benchmarking utilities"""

    @staticmethod
    def time_function(func: Callable, number: int = 1000) -> float:
        """Time a function execution"""
        timer = timeit.Timer(lambda: func())
        return timer.timeit(number=number) / number

    @staticmethod
    def compare_functions(functions: dict, number: int = 1000):
        """Compare multiple function implementations"""
        results = {}

        for name, func in functions.items():
            time_taken = Benchmark.time_function(func, number)
            results[name] = time_taken

        # Sort by time
        sorted_results = sorted(results.items(), key=lambda x: x[1])

        print("=" * 60)
        print(f"Benchmark Results ({number} iterations)")
        print("=" * 60)

        fastest_time = sorted_results[0][1]
        for name, time_taken in sorted_results:
            speedup = time_taken / fastest_time
            print(f"{name:30} {time_taken*1000:10.4f}ms  ({speedup:5.2f}x)")

        return results

    @staticmethod
    def benchmark_with_stats(func: Callable, runs: int = 100):
        """Run multiple times and get statistics"""
        times = []

        for _ in range(runs):
            start = timeit.default_timer()
            func()
            end = timeit.default_timer()
            times.append(end - start)

        return {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times)
        }

# Example: Compare list vs generator
def list_comp():
    return sum([i**2 for i in range(10000)])

def generator_exp():
    return sum(i**2 for i in range(10000))

def map_func():
    return sum(map(lambda x: x**2, range(10000)))

Benchmark.compare_functions({
    'List Comprehension': list_comp,
    'Generator Expression': generator_exp,
    'Map Function': map_func
})

# Detailed statistics
stats = Benchmark.benchmark_with_stats(list_comp, runs=100)
print(f"\nStatistics:")
print(f"Mean: {stats['mean']*1000:.4f}ms")
print(f"Median: {stats['median']*1000:.4f}ms")
print(f"StdDev: {stats['stdev']*1000:.4f}ms")
```

---

## 2. Memory Optimization

### 2.1 memory_profiler - Memory Usage Profiling

```python
# Install: pip install memory_profiler

from memory_profiler import profile
import sys

@profile
def memory_intensive_function():
    """Profile memory usage line by line"""
    # Large list
    big_list = [i for i in range(1000000)]

    # Dictionary
    big_dict = {i: i**2 for i in range(1000000)}

    # Process
    result = [x * 2 for x in big_list if x % 2 == 0]

    return result

# Run with: python -m memory_profiler script.py

# Check object size
def get_size(obj):
    """Get memory size of object"""
    size = sys.getsizeof(obj)

    if isinstance(obj, dict):
        size += sum([get_size(k) + get_size(v) for k, v in obj.items()])
    elif isinstance(obj, (list, tuple, set)):
        size += sum([get_size(item) for item in obj])

    return size

# Example
my_list = list(range(1000))
print(f"List size: {get_size(my_list):,} bytes")

my_dict = {i: i**2 for i in range(1000)}
print(f"Dict size: {get_size(my_dict):,} bytes")
```

### 2.2 Memory Optimization Techniques

```python
import sys
from array import array
import numpy as np

class MemoryOptimizer:
    """Memory optimization techniques"""

    @staticmethod
    def compare_data_structures():
        """Compare memory usage of different structures"""

        # List of integers
        list_data = list(range(1000000))
        list_size = sys.getsizeof(list_data)

        # Array of integers (much more efficient!)
        array_data = array('i', range(1000000))
        array_size = sys.getsizeof(array_data)

        # NumPy array (even better!)
        numpy_data = np.arange(1000000, dtype=np.int32)
        numpy_size = numpy_data.nbytes

        print(f"List:  {list_size:,} bytes")
        print(f"Array: {array_size:,} bytes ({list_size/array_size:.1f}x smaller)")
        print(f"NumPy: {numpy_size:,} bytes ({list_size/numpy_size:.1f}x smaller)")

    @staticmethod
    def use_generators():
        """Generators use minimal memory"""

        # Bad: Creates entire list in memory
        def get_numbers_list(n):
            return [i**2 for i in range(n)]

        # Good: Generates on demand
        def get_numbers_generator(n):
            for i in range(n):
                yield i**2

        # Compare
        list_result = get_numbers_list(1000000)
        gen_result = get_numbers_generator(1000000)

        print(f"List size: {sys.getsizeof(list_result):,} bytes")
        print(f"Generator size: {sys.getsizeof(gen_result):,} bytes")

    @staticmethod
    def use_slots():
        """__slots__ reduces memory for classes"""

        # Without __slots__
        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        # With __slots__ (much more efficient!)
        class PersonOptimized:
            __slots__ = ['name', 'age']

            def __init__(self, name, age):
                self.name = name
                self.age = age

        # Compare
        person = Person("John", 30)
        person_opt = PersonOptimized("John", 30)

        print(f"Person: {sys.getsizeof(person.__dict__):,} bytes")
        print(f"PersonOptimized: {sys.getsizeof(person_opt):,} bytes")

        # For 1 million objects, __slots__ saves ~40MB!

MemoryOptimizer.compare_data_structures()
MemoryOptimizer.use_generators()
MemoryOptimizer.use_slots()
```

### 2.3 Context Managers for Resource Management

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(name: str):
    """Context manager for timing code blocks"""
    start = time.time()
    yield
    end = time.time()
    print(f"{name}: {(end - start)*1000:.2f}ms")

@contextmanager
def memory_tracker(name: str):
    """Track memory usage of code block"""
    import tracemalloc

    tracemalloc.start()
    yield
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"{name}:")
    print(f"  Current: {current / 1024 / 1024:.2f} MB")
    print(f"  Peak: {peak / 1024 / 1024:.2f} MB")

# Usage
with timer("Data processing"):
    data = [i**2 for i in range(1000000)]

with memory_tracker("Large list creation"):
    big_list = [i for i in range(1000000)]
```

---

## 3. Algorithm Optimization

### 3.1 Big O Complexity Examples

```python
import time
from typing import List

class AlgorithmOptimization:
    """Demonstrate algorithm complexity improvements"""

    # O(n²) - Slow
    @staticmethod
    def find_duplicates_slow(arr: List[int]) -> List[int]:
        """Find duplicates - O(n²) nested loops"""
        duplicates = []
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] == arr[j] and arr[i] not in duplicates:
                    duplicates.append(arr[i])
        return duplicates

    # O(n) - Fast
    @staticmethod
    def find_duplicates_fast(arr: List[int]) -> List[int]:
        """Find duplicates - O(n) using set"""
        seen = set()
        duplicates = set()

        for num in arr:
            if num in seen:
                duplicates.add(num)
            else:
                seen.add(num)

        return list(duplicates)

    # O(n²) - Slow
    @staticmethod
    def has_pair_sum_slow(arr: List[int], target: int) -> bool:
        """Check if two numbers sum to target - O(n²)"""
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] + arr[j] == target:
                    return True
        return False

    # O(n) - Fast
    @staticmethod
    def has_pair_sum_fast(arr: List[int], target: int) -> bool:
        """Check if two numbers sum to target - O(n)"""
        seen = set()
        for num in arr:
            if target - num in seen:
                return True
            seen.add(num)
        return False

    # String concatenation - Slow
    @staticmethod
    def concat_strings_slow(strings: List[str]) -> str:
        """String concatenation - O(n²) due to string immutability"""
        result = ""
        for s in strings:
            result += s  # Creates new string each time!
        return result

    # String concatenation - Fast
    @staticmethod
    def concat_strings_fast(strings: List[str]) -> str:
        """String concatenation - O(n) using join"""
        return ''.join(strings)

# Benchmark
test_data = list(range(1000)) * 10  # 10,000 elements with duplicates

# Compare duplicate finding
start = time.time()
slow_result = AlgorithmOptimization.find_duplicates_slow(test_data)
slow_time = time.time() - start

start = time.time()
fast_result = AlgorithmOptimization.find_duplicates_fast(test_data)
fast_time = time.time() - start

print(f"Find Duplicates:")
print(f"  Slow (O(n²)): {slow_time*1000:.2f}ms")
print(f"  Fast (O(n)):  {fast_time*1000:.2f}ms")
print(f"  Speedup: {slow_time/fast_time:.1f}x faster")

# String concatenation benchmark
strings = ['x' * 100] * 1000

start = time.time()
AlgorithmOptimization.concat_strings_slow(strings)
slow_time = time.time() - start

start = time.time()
AlgorithmOptimization.concat_strings_fast(strings)
fast_time = time.time() - start

print(f"\nString Concatenation:")
print(f"  Slow (+= operator): {slow_time*1000:.2f}ms")
print(f"  Fast (join):        {fast_time*1000:.2f}ms")
print(f"  Speedup: {slow_time/fast_time:.1f}x faster")
```

### 3.2 Data Structure Selection

```python
import time
from collections import deque, Counter
from typing import List

class DataStructurePerformance:
    """Choose the right data structure for the job"""

    @staticmethod
    def list_vs_set_lookup():
        """Set lookup is O(1), list is O(n)"""
        data_list = list(range(100000))
        data_set = set(range(100000))

        # List lookup - O(n)
        start = time.time()
        for _ in range(1000):
            99999 in data_list
        list_time = time.time() - start

        # Set lookup - O(1)
        start = time.time()
        for _ in range(1000):
            99999 in data_set
        set_time = time.time() - start

        print(f"Membership test (1000 iterations):")
        print(f"  List: {list_time*1000:.2f}ms")
        print(f"  Set:  {set_time*1000:.2f}ms")
        print(f"  Speedup: {list_time/set_time:.0f}x faster\n")

    @staticmethod
    def list_vs_deque_operations():
        """deque is faster for inserting at start"""
        n = 100000

        # List - insert at start is O(n)
        start = time.time()
        test_list = []
        for i in range(n):
            test_list.insert(0, i)  # Slow!
        list_time = time.time() - start

        # Deque - insert at start is O(1)
        start = time.time()
        test_deque = deque()
        for i in range(n):
            test_deque.appendleft(i)  # Fast!
        deque_time = time.time() - start

        print(f"Insert at start ({n} operations):")
        print(f"  List:  {list_time*1000:.2f}ms")
        print(f"  Deque: {deque_time*1000:.2f}ms")
        print(f"  Speedup: {list_time/deque_time:.0f}x faster\n")

    @staticmethod
    def counting_optimization():
        """Counter is faster than manual counting"""
        data = [1, 2, 3, 1, 2, 1, 3, 4, 5, 1, 2] * 10000

        # Manual counting - Slow
        start = time.time()
        counts = {}
        for item in data:
            counts[item] = counts.get(item, 0) + 1
        manual_time = time.time() - start

        # Counter - Fast
        start = time.time()
        counts = Counter(data)
        counter_time = time.time() - start

        print(f"Counting elements:")
        print(f"  Manual: {manual_time*1000:.2f}ms")
        print(f"  Counter: {counter_time*1000:.2f}ms")
        print(f"  Speedup: {manual_time/counter_time:.1f}x faster\n")

# Run demonstrations
perf = DataStructurePerformance()
perf.list_vs_set_lookup()
perf.list_vs_deque_operations()
perf.counting_optimization()
```

---

## 4. Caching Strategies

### 4.1 Function Caching with functools

```python
from functools import lru_cache, cache
import time

class CachingExamples:
    """Demonstrate caching for performance"""

    # Without caching - Slow
    @staticmethod
    def fibonacci_slow(n: int) -> int:
        """Fibonacci without caching - O(2^n)"""
        if n < 2:
            return n
        return CachingExamples.fibonacci_slow(n-1) + CachingExamples.fibonacci_slow(n-2)

    # With LRU cache - Fast
    @staticmethod
    @lru_cache(maxsize=128)
    def fibonacci_fast(n: int) -> int:
        """Fibonacci with caching - O(n)"""
        if n < 2:
            return n
        return CachingExamples.fibonacci_fast(n-1) + CachingExamples.fibonacci_fast(n-2)

    # Python 3.9+: @cache decorator (unlimited size)
    @staticmethod
    @cache
    def expensive_computation(x: int, y: int) -> int:
        """Cache results of expensive computation"""
        time.sleep(0.1)  # Simulate expensive operation
        return x ** y

# Compare performance
print("Fibonacci(35):")

start = time.time()
result_slow = CachingExamples.fibonacci_slow(35)
slow_time = time.time() - start

start = time.time()
result_fast = CachingExamples.fibonacci_fast(35)
fast_time = time.time() - start

print(f"  Without cache: {slow_time:.3f}s")
print(f"  With cache:    {fast_time:.6f}s")
print(f"  Speedup: {slow_time/fast_time:.0f}x faster")

# Check cache stats
print(f"\nCache stats: {CachingExamples.fibonacci_fast.cache_info()}")

# Clear cache if needed
CachingExamples.fibonacci_fast.cache_clear()
```

### 4.2 Custom Cache Implementation

```python
from typing import Any, Callable
import time
from datetime import datetime, timedelta
import pickle

class Cache:
    """Custom cache with TTL (Time To Live)"""

    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl = ttl_seconds

    def get(self, key: str) -> Any:
        """Get value from cache"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            # Check if expired
            if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                return value
            else:
                # Remove expired entry
                del self.cache[key]
        return None

    def set(self, key: str, value: Any):
        """Set value in cache"""
        self.cache[key] = (value, datetime.now())

    def clear(self):
        """Clear all cache"""
        self.cache.clear()

    def cached(self, ttl_seconds: int = None):
        """Decorator to cache function results"""
        ttl = ttl_seconds or self.ttl

        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                # Create cache key from function name and arguments
                key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

                # Check cache
                cached_value = self.get(key)
                if cached_value is not None:
                    print(f"Cache HIT: {func.__name__}")
                    return cached_value

                # Compute and cache
                print(f"Cache MISS: {func.__name__}")
                result = func(*args, **kwargs)
                self.set(key, result)
                return result

            return wrapper
        return decorator

# Usage
cache = Cache(ttl_seconds=5)  # 5 second TTL

@cache.cached()
def fetch_data(user_id: int):
    """Simulate expensive API call"""
    print(f"  Fetching data for user {user_id}...")
    time.sleep(2)  # Simulate network delay
    return {'user_id': user_id, 'name': f'User {user_id}'}

# First call - cache miss
print("First call:")
data1 = fetch_data(123)

# Second call - cache hit!
print("\nSecond call (within TTL):")
data2 = fetch_data(123)

# Wait for expiration
print("\nWaiting 6 seconds for cache to expire...")
time.sleep(6)

# Third call - cache miss (expired)
print("Third call (after TTL):")
data3 = fetch_data(123)
```

### 4.3 Redis Caching (Production)

```python
import redis
import json
import pickle
from typing import Any, Optional
from functools import wraps

class RedisCache:
    """Production Redis caching"""

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=False  # Store bytes
        )

    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        data = self.redis.get(key)
        if data:
            return pickle.loads(data)
        return None

    def set(self, key: str, value: Any, ttl: int = 300):
        """Set value in Redis with TTL"""
        self.redis.setex(
            key,
            ttl,
            pickle.dumps(value)
        )

    def delete(self, key: str):
        """Delete key from Redis"""
        self.redis.delete(key)

    def cached(self, ttl: int = 300, key_prefix: str = ''):
        """Decorator for caching function results in Redis"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key
                cache_key = f"{key_prefix}{func.__name__}:{str(args)}:{str(kwargs)}"

                # Try to get from cache
                cached_value = self.get(cache_key)
                if cached_value is not None:
                    return cached_value

                # Compute and cache
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result

            # Add cache management methods
            wrapper.cache_clear = lambda: self.delete(f"{key_prefix}{func.__name__}:*")
            return wrapper
        return decorator

# Usage
redis_cache = RedisCache()

@redis_cache.cached(ttl=600, key_prefix='api:')
def get_user_data(user_id: int):
    """Get user data (cached for 10 minutes)"""
    # Expensive database query
    time.sleep(1)
    return {'id': user_id, 'name': f'User {user_id}'}

# First call - cache miss
data = get_user_data(123)

# Second call - cache hit from Redis
data = get_user_data(123)
```

---

## 5. Database Optimization

### 5.1 Query Optimization

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, joinedload, subqueryload
import time

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True)  # Index for fast lookups
    email = Column(String(100), index=True)
    posts = relationship('Post', back_populates='author')

    # Composite index for common query pattern
    __table_args__ = (
        Index('idx_username_email', 'username', 'email'),
    )

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(String(5000))
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    author = relationship('User', back_populates='posts')

class DatabaseOptimization:
    """Database query optimization techniques"""

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    # ❌ N+1 Query Problem (BAD)
    def get_users_with_posts_slow(self):
        """N+1 queries - SLOW!"""
        users = self.session.query(User).all()  # 1 query

        for user in users:
            posts = user.posts  # N queries (one per user)!
            print(f"{user.username}: {len(posts)} posts")

    # ✅ Eager Loading (GOOD)
    def get_users_with_posts_fast(self):
        """Eager loading - single query"""
        users = self.session.query(User).options(
            joinedload(User.posts)  # Load posts in same query!
        ).all()

        for user in users:
            posts = user.posts  # No additional query
            print(f"{user.username}: {len(posts)} posts")

    # Pagination for large results
    def get_users_paginated(self, page: int = 1, per_page: int = 20):
        """Paginate results instead of loading all"""
        offset = (page - 1) * per_page

        users = self.session.query(User)\
            .limit(per_page)\
            .offset(offset)\
            .all()

        return users

    # Select only needed columns
    def get_user_names_only(self):
        """Select only needed columns"""
        # Bad: SELECT * FROM users
        users = self.session.query(User).all()

        # Good: SELECT username FROM users
        usernames = self.session.query(User.username).all()

        return usernames

    # Bulk operations
    def bulk_insert_users(self, users_data: list):
        """Bulk insert is much faster"""
        # Slow: Insert one by one
        # for data in users_data:
        #     user = User(**data)
        #     self.session.add(user)
        #     self.session.commit()  # Commit each time!

        # Fast: Bulk insert
        self.session.bulk_insert_mappings(User, users_data)
        self.session.commit()  # Single commit

    # Use database functions
    def get_user_count(self):
        """Use COUNT in database, not Python"""
        # Slow: Load all and count in Python
        # users = self.session.query(User).all()
        # count = len(users)

        # Fast: COUNT in database
        count = self.session.query(User).count()
        return count
```

### 5.2 Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Configure connection pool
engine = create_engine(
    'postgresql://user:password@localhost/dbname',
    poolclass=QueuePool,
    pool_size=20,          # Number of connections to maintain
    max_overflow=10,       # Allow 10 additional connections
    pool_timeout=30,       # Timeout waiting for connection
    pool_recycle=3600,     # Recycle connections after 1 hour
    pool_pre_ping=True,    # Verify connections before using
)

# Connection pool stats
print(f"Pool size: {engine.pool.size()}")
print(f"Checked out: {engine.pool.checkedout()}")
```

---

## 6. Async Programming for Performance

### 6.1 asyncio Basics

```python
import asyncio
import aiohttp
import time
from typing import List

class AsyncPerformance:
    """Asynchronous programming for I/O-bound tasks"""

    # Synchronous (slow)
    @staticmethod
    def fetch_url_sync(url: str) -> str:
        """Fetch URL synchronously"""
        import requests
        response = requests.get(url)
        return response.text

    @staticmethod
    def fetch_multiple_sync(urls: List[str]):
        """Fetch multiple URLs synchronously - SLOW"""
        start = time.time()
        results = []

        for url in urls:
            results.append(AsyncPerformance.fetch_url_sync(url))

        elapsed = time.time() - start
        print(f"Synchronous: {elapsed:.2f}s for {len(urls)} URLs")
        return results

    # Asynchronous (fast)
    @staticmethod
    async def fetch_url_async(url: str, session: aiohttp.ClientSession) -> str:
        """Fetch URL asynchronously"""
        async with session.get(url) as response:
            return await response.text()

    @staticmethod
    async def fetch_multiple_async(urls: List[str]):
        """Fetch multiple URLs asynchronously - FAST"""
        start = time.time()

        async with aiohttp.ClientSession() as session:
            tasks = [
                AsyncPerformance.fetch_url_async(url, session)
                for url in urls
            ]
            results = await asyncio.gather(*tasks)

        elapsed = time.time() - start
        print(f"Asynchronous: {elapsed:.2f}s for {len(urls)} URLs")
        return results

# Example: Fetch 10 URLs
urls = [
    'http://httpbin.org/delay/1',
    'http://httpbin.org/delay/1',
    'http://httpbin.org/delay/1',
] * 3  # 9 URLs total

# Synchronous: ~9 seconds (sequential)
# AsyncPerformance.fetch_multiple_sync(urls)

# Asynchronous: ~1 second (parallel)
asyncio.run(AsyncPerformance.fetch_multiple_async(urls))
```

### 6.2 Async Database Queries

```python
from databases import Database
import asyncio

# Using databases library for async database access
database = Database('postgresql://user:pass@localhost/db')

async def fetch_users_async():
    """Async database queries"""
    await database.connect()

    # Fetch multiple queries in parallel
    users_task = database.fetch_all("SELECT * FROM users")
    posts_task = database.fetch_all("SELECT * FROM posts")
    comments_task = database.fetch_all("SELECT * FROM comments")

    # Wait for all to complete
    users, posts, comments = await asyncio.gather(
        users_task,
        posts_task,
        comments_task
    )

    await database.disconnect()
    return users, posts, comments

# Run
# asyncio.run(fetch_users_async())
```

---

## 7. Parallel Processing

### 7.1 Multiprocessing for CPU-Bound Tasks

```python
from multiprocessing import Pool, cpu_count
import time
from typing import List

class ParallelProcessing:
    """Multiprocessing for CPU-intensive tasks"""

    @staticmethod
    def expensive_computation(n: int) -> int:
        """CPU-intensive task"""
        total = 0
        for i in range(n):
            total += i ** 2
        return total

    @staticmethod
    def process_sequential(numbers: List[int]):
        """Process sequentially - SLOW"""
        start = time.time()

        results = [
            ParallelProcessing.expensive_computation(n)
            for n in numbers
        ]

        elapsed = time.time() - start
        print(f"Sequential: {elapsed:.2f}s")
        return results

    @staticmethod
    def process_parallel(numbers: List[int]):
        """Process in parallel - FAST"""
        start = time.time()

        # Use all CPU cores
        with Pool(cpu_count()) as pool:
            results = pool.map(
                ParallelProcessing.expensive_computation,
                numbers
            )

        elapsed = time.time() - start
        print(f"Parallel ({cpu_count()} cores): {elapsed:.2f}s")
        return results

# Example
numbers = [10000000] * 8

# Sequential: ~8 seconds
ParallelProcessing.process_sequential(numbers)

# Parallel: ~2 seconds (4x faster on 4-core CPU)
ParallelProcessing.process_parallel(numbers)
```

### 7.2 ThreadPoolExecutor for I/O-Bound Tasks

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import requests

class ThreadingPerformance:
    """Threading for I/O-bound tasks"""

    @staticmethod
    def download_file(url: str) -> int:
        """Download file and return size"""
        response = requests.get(url)
        return len(response.content)

    @staticmethod
    def download_sequential(urls: List[str]):
        """Download files sequentially"""
        start = time.time()

        sizes = []
        for url in urls:
            size = ThreadingPerformance.download_file(url)
            sizes.append(size)

        elapsed = time.time() - start
        print(f"Sequential: {elapsed:.2f}s")
        return sizes

    @staticmethod
    def download_parallel(urls: List[str], max_workers: int = 10):
        """Download files in parallel"""
        start = time.time()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            sizes = list(executor.map(
                ThreadingPerformance.download_file,
                urls
            ))

        elapsed = time.time() - start
        print(f"Parallel ({max_workers} threads): {elapsed:.2f}s")
        return sizes

# Example
urls = ['http://httpbin.org/image/png'] * 20

# Sequential: ~20 seconds
# ThreadingPerformance.download_sequential(urls)

# Parallel: ~2 seconds
# ThreadingPerformance.download_parallel(urls)
```

---

## 8. NumPy & Pandas Optimization

### 8.1 NumPy Vectorization

```python
import numpy as np
import time

class NumPyOptimization:
    """NumPy optimization techniques"""

    @staticmethod
    def python_loops_slow():
        """Pure Python loops - SLOW"""
        data = list(range(1000000))

        start = time.time()
        result = [x ** 2 for x in data]
        python_time = time.time() - start

        return python_time

    @staticmethod
    def numpy_vectorized_fast():
        """NumPy vectorized operations - FAST"""
        data = np.arange(1000000)

        start = time.time()
        result = data ** 2  # Vectorized!
        numpy_time = time.time() - start

        return numpy_time

# Compare
python_time = NumPyOptimization.python_loops_slow()
numpy_time = NumPyOptimization.numpy_vectorized_fast()

print(f"Python loops: {python_time*1000:.2f}ms")
print(f"NumPy vectorized: {numpy_time*1000:.2f}ms")
print(f"Speedup: {python_time/numpy_time:.0f}x faster")
```

### 8.2 Pandas Optimization

```python
import pandas as pd
import numpy as np

class PandasOptimization:
    """Pandas performance tips"""

    @staticmethod
    def use_vectorization():
        """Avoid loops, use vectorized operations"""
        df = pd.DataFrame({
            'A': np.random.randint(0, 100, 1000000),
            'B': np.random.randint(0, 100, 1000000)
        })

        # Slow: iterating rows
        start = time.time()
        results = []
        for idx, row in df.iterrows():
            results.append(row['A'] + row['B'])
        slow_time = time.time() - start

        # Fast: vectorized
        start = time.time()
        results = df['A'] + df['B']
        fast_time = time.time() - start

        print(f"iterrows: {slow_time:.2f}s")
        print(f"Vectorized: {fast_time:.4f}s")
        print(f"Speedup: {slow_time/fast_time:.0f}x faster")

    @staticmethod
    def optimize_dtypes():
        """Use appropriate data types"""
        df = pd.DataFrame({
            'int_col': range(1000000),
            'float_col': np.random.rand(1000000),
            'category_col': np.random.choice(['A', 'B', 'C'], 1000000)
        })

        print(f"Original memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

        # Optimize
        df['int_col'] = df['int_col'].astype('int32')  # int64 → int32
        df['float_col'] = df['float_col'].astype('float32')  # float64 → float32
        df['category_col'] = df['category_col'].astype('category')  # object → category

        print(f"Optimized memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

PandasOptimization.use_vectorization()
PandasOptimization.optimize_dtypes()
```

---

## 9. Python Performance Tips

```python
# 1. Use local variables (faster than global)
def fast_function():
    local_var = 10  # Faster access
    return local_var + 5

# 2. Use built-in functions (written in C)
# Fast: sum(numbers)
# Slow: reduce(lambda x, y: x + y, numbers)

# 3. Avoid global keyword
x = 10
def slow():
    global x  # Slow
    x += 1

def fast():
    y = x  # Fast - local copy
    y += 1
    return y

# 4. Use list comprehensions
# Fast: [x**2 for x in range(1000)]
# Slow: list(map(lambda x: x**2, range(1000)))

# 5. Reuse objects
# Fast:
result = []
for i in range(1000):
    result.append(i)

# Slow:
for i in range(1000):
    result = result + [i]  # Creates new list!

# 6. Use __slots__ for classes
class Fast:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 7. Profile before optimizing!
# Don't guess - measure!
```

---

## 10. Production Performance Monitoring

```python
import time
import psutil
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Prometheus metrics
request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
memory_usage = Gauge('memory_usage_bytes', 'Memory usage in bytes')
cpu_usage = Gauge('cpu_usage_percent', 'CPU usage percentage')

def monitor_performance():
    """Monitor application performance"""
    while True:
        # Update metrics
        memory_usage.set(psutil.virtual_memory().used)
        cpu_usage.set(psutil.cpu_percent())

        time.sleep(5)

# Start metrics server
# start_http_server(8000)
# Metrics available at http://localhost:8000/metrics
```

---

## Performance Optimization Checklist

### ✅ Always Do

1. **Profile first** - Don't optimize without measuring
2. **Use appropriate data structures** - set for lookups, deque for queues
3. **Cache expensive operations** - @lru_cache, Redis
4. **Use generators** for large datasets
5. **Vectorize with NumPy** - 10-100x faster than loops
6. **Use async for I/O** - Massive speedup for network/disk
7. **Index database columns** - 1000x faster queries
8. **Use connection pooling** - Reuse database connections
9. **Paginate large results** - Don't load everything at once
10. **Monitor in production** - Prometheus, New Relic

### ❌ Never Do

1. **Never optimize prematurely** - Profile first!
2. **Never use loops on DataFrames** - Use vectorization
3. **Never load all data into memory** - Stream or paginate
4. **Never ignore Big O complexity** - Algorithm choice matters most
5. **Never concatenate strings in loops** - Use join()
6. **Never use multiprocessing for I/O** - Use async instead
7. **Never forget to close resources** - Use context managers
8. **Never ignore database indexes** - Add indexes for frequent queries

This comprehensive guide covers all essential Python performance optimization techniques for professional development!
