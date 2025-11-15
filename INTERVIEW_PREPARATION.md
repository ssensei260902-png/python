# 🎯 Python Developer Interview Preparation Guide

## Complete Guide to Ace Technical Interviews

---

## Table of Contents

1. [Coding Interview Patterns](#1-coding-interview-patterns)
2. [Data Structures & Algorithms](#2-data-structures--algorithms)
3. [System Design Interview](#3-system-design-interview)
4. [Python-Specific Questions](#4-python-specific-questions)
5. [Behavioral Interview](#5-behavioral-interview)
6. [Coding Challenge Solutions](#6-coding-challenge-solutions)
7. [Interview Tips & Strategies](#7-interview-tips--strategies)

---

## 1. Coding Interview Patterns

### 1.1 Two Pointers Pattern

```python
def two_sum_sorted(nums: List[int], target: int) -> List[int]:
    """
    Find two numbers that sum to target in sorted array
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left < right:
        current_sum = nums[left] + nums[right]

        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return []


def remove_duplicates(nums: List[int]) -> int:
    """
    Remove duplicates from sorted array in-place
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0

    write_pointer = 1

    for read_pointer in range(1, len(nums)):
        if nums[read_pointer] != nums[read_pointer - 1]:
            nums[write_pointer] = nums[read_pointer]
            write_pointer += 1

    return write_pointer


def is_palindrome(s: str) -> bool:
    """
    Check if string is palindrome (ignoring non-alphanumeric)
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
```

### 1.2 Sliding Window Pattern

```python
def max_sum_subarray(nums: List[int], k: int) -> int:
    """
    Find maximum sum of subarray of size k
    Time: O(n), Space: O(1)
    """
    if len(nums) < k:
        return 0

    # Initialize window
    window_sum = sum(nums[:k])
    max_sum = window_sum

    # Slide window
    for i in range(k, len(nums)):
        window_sum = window_sum - nums[i - k] + nums[i]
        max_sum = max(max_sum, window_sum)

    return max_sum


def longest_substring_without_repeating(s: str) -> int:
    """
    Find length of longest substring without repeating characters
    Time: O(n), Space: O(min(n, m)) where m is charset size
    """
    char_index = {}
    max_length = 0
    start = 0

    for end, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1

        char_index[char] = end
        max_length = max(max_length, end - start + 1)

    return max_length


def min_window_substring(s: str, t: str) -> str:
    """
    Minimum window substring containing all characters of t
    Time: O(|s| + |t|), Space: O(|t|)
    """
    from collections import Counter

    if not s or not t:
        return ""

    # Character frequency in t
    required = Counter(t)
    required_count = len(required)

    # Sliding window
    left = right = 0
    formed = 0
    window_counts = {}

    # Result: (window length, left, right)
    result = float('inf'), None, None

    while right < len(s):
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1

        if char in required and window_counts[char] == required[char]:
            formed += 1

        # Try to shrink window
        while left <= right and formed == required_count:
            char = s[left]

            # Update result
            if right - left + 1 < result[0]:
                result = (right - left + 1, left, right)

            window_counts[char] -= 1
            if char in required and window_counts[char] < required[char]:
                formed -= 1

            left += 1

        right += 1

    return "" if result[0] == float('inf') else s[result[1]:result[2] + 1]
```

### 1.3 Fast & Slow Pointers (Floyd's Algorithm)

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def has_cycle(head: ListNode) -> bool:
    """
    Detect cycle in linked list
    Time: O(n), Space: O(1)
    """
    if not head:
        return False

    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False


def find_cycle_start(head: ListNode) -> ListNode:
    """
    Find start of cycle in linked list
    Time: O(n), Space: O(1)
    """
    if not head:
        return None

    # Find meeting point
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            break
    else:
        return None  # No cycle

    # Find cycle start
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow


def middle_of_linked_list(head: ListNode) -> ListNode:
    """
    Find middle node of linked list
    Time: O(n), Space: O(1)
    """
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow
```

### 1.4 Binary Search Pattern

```python
def binary_search(nums: List[int], target: int) -> int:
    """
    Standard binary search
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def find_first_occurrence(nums: List[int], target: int) -> int:
    """
    Find first occurrence of target
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            result = mid
            right = mid - 1  # Continue searching left
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def search_rotated_sorted_array(nums: List[int], target: int) -> int:
    """
    Search in rotated sorted array
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        # Determine which half is sorted
        if nums[left] <= nums[mid]:
            # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1
```

---

## 2. Data Structures & Algorithms

### 2.1 Tree Traversals

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def inorder_traversal(root: TreeNode) -> List[int]:
    """
    Inorder: Left -> Root -> Right
    Time: O(n), Space: O(h) where h is height
    """
    result = []

    def traverse(node):
        if not node:
            return

        traverse(node.left)
        result.append(node.val)
        traverse(node.right)

    traverse(root)
    return result


def level_order_traversal(root: TreeNode) -> List[List[int]]:
    """
    Level-order (BFS) traversal
    Time: O(n), Space: O(w) where w is max width
    """
    if not root:
        return []

    from collections import deque

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result


def max_depth(root: TreeNode) -> int:
    """
    Maximum depth of binary tree
    Time: O(n), Space: O(h)
    """
    if not root:
        return 0

    return 1 + max(max_depth(root.left), max_depth(root.right))


def is_valid_bst(root: TreeNode) -> bool:
    """
    Validate Binary Search Tree
    Time: O(n), Space: O(h)
    """
    def validate(node, min_val, max_val):
        if not node:
            return True

        if not (min_val < node.val < max_val):
            return False

        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))

    return validate(root, float('-inf'), float('inf'))


def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Find LCA of two nodes
    Time: O(n), Space: O(h)
    """
    if not root or root == p or root == q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    if left and right:
        return root

    return left if left else right
```

### 2.2 Dynamic Programming

```python
def fibonacci_dp(n: int) -> int:
    """
    Fibonacci with DP
    Time: O(n), Space: O(1)
    """
    if n <= 1:
        return n

    prev, curr = 0, 1

    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr

    return curr


def longest_increasing_subsequence(nums: List[int]) -> int:
    """
    Length of longest increasing subsequence
    Time: O(n²), Space: O(n)
    """
    if not nums:
        return 0

    dp = [1] * len(nums)

    for i in range(1, len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


def coin_change(coins: List[int], amount: int) -> int:
    """
    Minimum coins to make amount
    Time: O(amount * len(coins)), Space: O(amount)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    """
    0/1 Knapsack problem
    Time: O(n * capacity), Space: O(capacity)
    """
    n = len(weights)
    dp = [0] * (capacity + 1)

    for i in range(n):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]


def edit_distance(word1: str, word2: str) -> int:
    """
    Minimum edit distance (Levenshtein distance)
    Time: O(m * n), Space: O(min(m, n))
    """
    m, n = len(word1), len(word2)

    # Optimize space by using only two rows
    prev = list(range(n + 1))

    for i in range(1, m + 1):
        curr = [i] + [0] * n

        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(
                    prev[j],      # Delete
                    curr[j - 1],  # Insert
                    prev[j - 1]   # Replace
                )

        prev = curr

    return prev[n]
```

---

## 3. System Design Interview

### 3.1 URL Shortener Design

```
Problem: Design a URL shortening service like bit.ly

Requirements:
- Given a long URL, generate a short unique URL
- Redirect short URL to original URL
- Handle 100M URLs
- High availability

Components:

1. API Design:
   - POST /api/shorten - Create short URL
   - GET /{shortCode} - Redirect to original URL

2. Database Schema:
   CREATE TABLE urls (
       id BIGINT PRIMARY KEY,
       short_code VARCHAR(10) UNIQUE,
       original_url VARCHAR(2048),
       created_at TIMESTAMP,
       expires_at TIMESTAMP,
       click_count INT
   );

   CREATE INDEX idx_short_code ON urls(short_code);

3. Short Code Generation:
   - Base62 encoding (a-z, A-Z, 0-9) = 62^7 = 3.5 trillion combinations
   - Use auto-incrementing ID converted to base62
   - Or use hash of URL (MD5) + take first 7 characters

4. Scalability:
   - Cache frequently accessed URLs in Redis
   - Distribute database (sharding by short_code hash)
   - Use CDN for global distribution
   - Load balancer for multiple app servers

5. High Availability:
   - Database replication (master-slave)
   - Redis cluster with replication
   - Multiple availability zones
```

### 3.2 Design Twitter Feed

```
Problem: Design Twitter newsfeed

Requirements:
- User can post tweets
- User can follow other users
- User sees tweets from followed users in chronological order
- Handle millions of users

Components:

1. Data Models:
   - Users: id, username, email
   - Tweets: id, user_id, content, created_at
   - Follows: follower_id, followee_id

2. Feed Generation Approaches:

   A. Pull Model (Read-time):
      - When user requests feed, query tweets from all followed users
      - Pros: Write simple, no fanout
      - Cons: Slow reads (must query many users)

   B. Push Model (Write-time):
      - When user posts tweet, push to all followers' feeds
      - Pros: Fast reads (pre-computed)
      - Cons: Slow writes for users with many followers

   C. Hybrid Model:
      - Push for normal users (<1000 followers)
      - Pull for celebrities (>1000 followers)
      - Merge at read time

3. Architecture:
   - API Gateway
   - Tweet Service (post tweets)
   - Feed Service (generate feed)
   - Timeline Cache (Redis)
   - Database (sharded by user_id)
   - Message Queue (Kafka) for async processing

4. Scalability:
   - Cache user timelines in Redis
   - Shard database by user_id
   - CDN for media files
   - Kafka for async tweet fanout
```

### 3.3 Design Rate Limiter

```
Problem: Design API rate limiter

Requirements:
- Limit requests per user/IP
- Support different limits (100/min, 1000/hour)
- Distributed system

Algorithms:

1. Token Bucket:
   class TokenBucket:
       def __init__(self, capacity, refill_rate):
           self.capacity = capacity
           self.tokens = capacity
           self.refill_rate = refill_rate
           self.last_refill = time.time()

       def allow_request(self):
           self._refill()
           if self.tokens >= 1:
               self.tokens -= 1
               return True
           return False

       def _refill(self):
           now = time.time()
           tokens_to_add = (now - self.last_refill) * self.refill_rate
           self.tokens = min(self.capacity, self.tokens + tokens_to_add)
           self.last_refill = now

2. Sliding Window Log:
   - Store timestamp of each request in Redis sorted set
   - Count requests in last window
   - Remove old requests

3. Sliding Window Counter:
   - Divide time into fixed windows
   - Weighted count of current + previous window

Implementation with Redis:
```

```python
import redis
import time

class RateLimiter:
    """Distributed rate limiter with Redis"""

    def __init__(self, redis_client):
        self.redis = redis_client

    def is_allowed(self, user_id: str, limit: int, window: int) -> bool:
        """
        Check if request is allowed
        limit: number of requests
        window: time window in seconds
        """
        key = f"rate_limit:{user_id}"
        now = time.time()

        # Remove old requests
        self.redis.zremrangebyscore(key, 0, now - window)

        # Count requests in window
        request_count = self.redis.zcard(key)

        if request_count < limit:
            # Add current request
            self.redis.zadd(key, {now: now})
            self.redis.expire(key, window)
            return True

        return False
```

---

## 4. Python-Specific Questions

### 4.1 Common Interview Questions

**Q: What is the difference between `is` and `==`?**
```python
# == checks value equality
# is checks identity (same object in memory)

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True (same values)
print(a is b)  # False (different objects)
print(a is c)  # True (same object)

# Special case: small integers and strings are interned
x = 5
y = 5
print(x is y)  # True (same object due to interning)
```

**Q: Explain generators and when to use them**
```python
# Generator: function that yields values one at a time
# Memory efficient for large datasets

def fibonacci_generator(n):
    """Generate fibonacci numbers"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Use generator
for num in fibonacci_generator(10):
    print(num)

# Generator expression (like list comprehension)
squares = (x**2 for x in range(1000000))  # Memory efficient
# vs
squares_list = [x**2 for x in range(1000000)]  # Loads all in memory
```

**Q: What are decorators?**
```python
# Decorator: function that modifies another function

def timer(func):
    """Measure execution time"""
    import time
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result

    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done"

slow_function()  # Prints execution time
```

**Q: Explain `*args` and `**kwargs`**
```python
def function_with_args(*args, **kwargs):
    """
    *args: variable number of positional arguments (tuple)
    **kwargs: variable number of keyword arguments (dict)
    """
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")

function_with_args(1, 2, 3, name="John", age=30)
# args: (1, 2, 3)
# kwargs: {'name': 'John', 'age': 30}
```

**Q: How does Python's GIL work?**
```
GIL (Global Interpreter Lock):
- Mutex that protects Python objects
- Only one thread executes Python bytecode at a time
- Affects CPU-bound multi-threaded programs
- I/O-bound programs not affected (releases GIL during I/O)

Solutions:
- Use multiprocessing for CPU-bound tasks
- Use async/await for I/O-bound tasks
- Use C extensions (release GIL)
```

---

## 5. Behavioral Interview

### STAR Method (Situation, Task, Action, Result)

**Example: "Tell me about a time you faced a technical challenge"**

```
Situation:
"At my previous company, we had a critical API endpoint that was timing out
under peak load, causing 20% of requests to fail."

Task:
"I was tasked with diagnosing and fixing the performance issue within one week
before our major product launch."

Action:
"I profiled the code and found that we were making N+1 database queries.
I implemented:
1. Query optimization with eager loading
2. Redis caching for frequently accessed data
3. Database indexing on commonly queried fields
4. Connection pooling to reduce overhead"

Result:
"The response time dropped from 3 seconds to 200ms, and we eliminated all
timeout errors. The fix also improved overall system performance by 40%,
and we successfully launched on time."
```

### Common Behavioral Questions

1. **"Why do you want to work here?"**
   - Research company's tech stack, products, culture
   - Mention specific technologies/projects that excite you
   - Align with company values

2. **"Tell me about a disagreement with a teammate"**
   - Focus on respectful communication
   - Emphasize finding data-driven solutions
   - Show you can compromise

3. **"Describe your biggest technical achievement"**
   - Use STAR method
   - Quantify impact (metrics, users, revenue)
   - Highlight technical skills used

4. **"How do you stay updated with technology?"**
   - Read blogs, documentation
   - Contribute to open source
   - Attend conferences/meetups
   - Build side projects

---

## 6. Coding Challenge Solutions

### Problem: LRU Cache

```python
from collections import OrderedDict

class LRUCache:
    """
    Least Recently Used Cache
    get() and put() in O(1) time
    """

    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update and move to end
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.capacity:
            # Remove least recently used (first item)
            self.cache.popitem(last=False)
```

### Problem: Serialize & Deserialize Binary Tree

```python
class Codec:
    """Serialize and deserialize binary tree"""

    def serialize(self, root: TreeNode) -> str:
        """Encode tree to string"""
        def helper(node):
            if not node:
                return 'null,'

            return f"{node.val},{helper(node.left)}{helper(node.right)}"

        return helper(root)

    def deserialize(self, data: str) -> TreeNode:
        """Decode string to tree"""
        def helper(nodes):
            val = next(nodes)

            if val == 'null':
                return None

            node = TreeNode(int(val))
            node.left = helper(nodes)
            node.right = helper(nodes)

            return node

        nodes = iter(data.split(','))
        return helper(nodes)
```

---

## 7. Interview Tips & Strategies

### Before the Interview

1. **Practice on platforms:**
   - LeetCode (1000+ problems)
   - HackerRank
   - CodeSignal
   - InterviewBit

2. **Study plan (8 weeks):**
   - Week 1-2: Arrays, Strings, Hash Tables
   - Week 3-4: Linked Lists, Trees, Graphs
   - Week 5-6: Dynamic Programming, Recursion
   - Week 7: System Design
   - Week 8: Mock interviews, review

3. **Mock interviews:**
   - Practice with friends
   - Pramp, interviewing.io
   - Record yourself coding

### During the Interview

1. **Clarify requirements:**
   - Ask about input size, edge cases
   - Confirm expected output format
   - Discuss time/space constraints

2. **Think out loud:**
   - Explain your thought process
   - Discuss trade-offs
   - Mention alternative approaches

3. **Start with brute force:**
   - Explain simple solution first
   - Then optimize
   - Analyze time/space complexity

4. **Test your code:**
   - Walk through with example
   - Check edge cases (empty input, single element, duplicates)
   - Fix bugs carefully

5. **Ask questions:**
   - Show curiosity about the team/tech stack
   - Ask about challenges they face
   - Inquire about growth opportunities

### Common Mistakes to Avoid

❌ Jumping to code immediately
❌ Not considering edge cases
❌ Ignoring time/space complexity
❌ Being silent while thinking
❌ Not testing code
❌ Giving up too quickly

✅ Clarify problem first
✅ Discuss approach before coding
✅ Think out loud
✅ Test thoroughly
✅ Ask for hints if stuck

---

## Practice Plan

**30 Days to Interview Success:**

**Week 1: Arrays & Strings**
- Two Sum, Three Sum
- Longest Substring Without Repeating Characters
- Trapping Rain Water

**Week 2: Linked Lists & Trees**
- Reverse Linked List
- Detect Cycle
- Binary Tree Level Order Traversal
- Validate BST

**Week 3: Graphs & Backtracking**
- Number of Islands
- Course Schedule
- Word Search
- N-Queens

**Week 4: DP & Review**
- Climbing Stairs
- Longest Increasing Subsequence
- Word Break
- Review all previous problems

**Daily Routine:**
- Morning: 1 hard problem (1 hour)
- Evening: 2 medium problems (1 hour)
- Night: Review solutions, study patterns (30 min)

---

## Resources

**Books:**
- "Cracking the Coding Interview" - Gayle Laakmann McDowell
- "Elements of Programming Interviews in Python"
- "System Design Interview" - Alex Xu

**Websites:**
- LeetCode.com
- HackerRank.com
- GeeksforGeeks.org
- InterviewBit.com

**YouTube Channels:**
- NeetCode
- Back To Back SWE
- Clément Mihailescu

**Practice everyday. Success = Preparation + Practice + Patience!**
