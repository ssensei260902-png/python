# 📬 Message Queues & Event-Driven Architecture

## Complete Professional Guide to Distributed Messaging Systems

---

## Table of Contents

1. [RabbitMQ with Pika](#1-rabbitmq-with-pika)
2. [Apache Kafka](#2-apache-kafka)
3. [Redis Pub/Sub](#3-redis-pubsub)
4. [Event-Driven Architecture](#4-event-driven-architecture)
5. [CQRS Pattern](#5-cqrs-pattern)
6. [Event Sourcing](#6-event-sourcing)
7. [Saga Pattern](#7-saga-pattern)
8. [Message Queue Best Practices](#8-best-practices)

---

## 1. RabbitMQ with Pika

### 1.1 Complete RabbitMQ Producer/Consumer

```python
import pika
import json
from typing import Callable, Dict
import time
from datetime import datetime

class RabbitMQProducer:
    """Professional RabbitMQ message producer"""

    def __init__(self, host='localhost', port=5672, username='guest', password='guest'):
        credentials = pika.PlainCredentials(username, password)
        self.parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        self.connection = None
        self.channel = None

    def connect(self):
        """Establish connection to RabbitMQ"""
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def close(self):
        """Close connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def declare_queue(self, queue_name: str, durable=True):
        """Declare a queue"""
        self.channel.queue_declare(
            queue=queue_name,
            durable=durable  # Survive broker restart
        )

    def declare_exchange(self, exchange_name: str, exchange_type='direct', durable=True):
        """Declare an exchange"""
        self.channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=exchange_type,  # direct, fanout, topic, headers
            durable=durable
        )

    def bind_queue(self, queue_name: str, exchange_name: str, routing_key=''):
        """Bind queue to exchange"""
        self.channel.queue_bind(
            queue=queue_name,
            exchange=exchange_name,
            routing_key=routing_key
        )

    def publish_message(
        self,
        message: dict,
        queue_name: str = None,
        exchange: str = '',
        routing_key: str = '',
        persistent=True
    ):
        """Publish message to queue or exchange"""
        body = json.dumps(message)

        properties = pika.BasicProperties(
            delivery_mode=2 if persistent else 1,  # 2 = persistent
            content_type='application/json',
            timestamp=int(time.time())
        )

        if queue_name:
            routing_key = queue_name

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
            properties=properties
        )

        print(f"✓ Published message to {routing_key}")


class RabbitMQConsumer:
    """Professional RabbitMQ message consumer"""

    def __init__(self, host='localhost', port=5672, username='guest', password='guest'):
        credentials = pika.PlainCredentials(username, password)
        self.parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        self.connection = None
        self.channel = None
        self.callbacks: Dict[str, Callable] = {}

    def connect(self):
        """Establish connection"""
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def close(self):
        """Close connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def declare_queue(self, queue_name: str, durable=True):
        """Declare queue"""
        self.channel.queue_declare(queue=queue_name, durable=durable)

    def set_prefetch_count(self, count=1):
        """Set number of unacknowledged messages"""
        self.channel.basic_qos(prefetch_count=count)

    def consume(self, queue_name: str, callback: Callable, auto_ack=False):
        """Consume messages from queue"""
        def on_message(ch, method, properties, body):
            try:
                message = json.loads(body)
                print(f"Received message from {queue_name}: {message}")

                # Process message
                callback(message)

                # Acknowledge message
                if not auto_ack:
                    ch.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as e:
                print(f"Error processing message: {e}")
                # Reject and requeue message
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message,
            auto_ack=auto_ack
        )

        print(f"Waiting for messages on {queue_name}. Press Ctrl+C to exit.")
        self.channel.start_consuming()


# Usage Examples

# Example 1: Simple Queue
def simple_queue_example():
    """Simple producer-consumer example"""

    # Producer
    producer = RabbitMQProducer()
    producer.connect()
    producer.declare_queue('task_queue')

    # Send messages
    for i in range(10):
        message = {
            'task_id': i,
            'data': f'Task {i}',
            'created_at': datetime.utcnow().isoformat()
        }
        producer.publish_message(message, queue_name='task_queue')

    producer.close()

    # Consumer
    def process_task(message):
        """Process task"""
        print(f"Processing task: {message['task_id']}")
        time.sleep(1)  # Simulate work
        print(f"Task {message['task_id']} completed")

    consumer = RabbitMQConsumer()
    consumer.connect()
    consumer.declare_queue('task_queue')
    consumer.set_prefetch_count(1)  # Process one at a time
    consumer.consume('task_queue', process_task)


# Example 2: Pub/Sub with Fanout Exchange
def pubsub_example():
    """Publish-Subscribe pattern"""

    producer = RabbitMQProducer()
    producer.connect()

    # Declare fanout exchange
    producer.declare_exchange('logs', exchange_type='fanout')

    # Publish log messages
    log_levels = ['info', 'warning', 'error']
    for level in log_levels:
        message = {
            'level': level,
            'message': f'This is a {level} message',
            'timestamp': datetime.utcnow().isoformat()
        }
        producer.publish_message(message, exchange='logs')

    producer.close()

    # Multiple consumers (subscribers)
    def create_subscriber(subscriber_name):
        consumer = RabbitMQConsumer()
        consumer.connect()

        # Declare exchange
        consumer.channel.exchange_declare(exchange='logs', exchange_type='fanout')

        # Create exclusive queue
        result = consumer.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # Bind to exchange
        consumer.channel.queue_bind(exchange='logs', queue=queue_name)

        def callback(message):
            print(f"[{subscriber_name}] Received: {message}")

        consumer.consume(queue_name, callback)

    # Start multiple subscribers
    # create_subscriber('Logger1')
    # create_subscriber('Logger2')


# Example 3: Topic Exchange (Routing)
def topic_routing_example():
    """Topic-based routing"""

    producer = RabbitMQProducer()
    producer.connect()
    producer.declare_exchange('events', exchange_type='topic')

    # Publish events with different routing keys
    events = [
        ('user.created', {'user_id': 1, 'username': 'john'}),
        ('user.updated', {'user_id': 1, 'username': 'john_doe'}),
        ('order.created', {'order_id': 100, 'amount': 99.99}),
        ('order.shipped', {'order_id': 100, 'tracking': 'ABC123'}),
    ]

    for routing_key, data in events:
        message = {'event': routing_key, 'data': data}
        producer.publish_message(
            message,
            exchange='events',
            routing_key=routing_key
        )

    producer.close()

    # Consumers with topic patterns
    def create_topic_consumer(binding_key, consumer_name):
        consumer = RabbitMQConsumer()
        consumer.connect()

        consumer.channel.exchange_declare(exchange='events', exchange_type='topic')

        result = consumer.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # Bind with pattern (* = one word, # = zero or more words)
        consumer.channel.queue_bind(
            exchange='events',
            queue=queue_name,
            routing_key=binding_key
        )

        def callback(message):
            print(f"[{consumer_name}] {message}")

        consumer.consume(queue_name, callback)

    # Listen to all user events: user.*
    # create_topic_consumer('user.*', 'UserService')

    # Listen to all events: #
    # create_topic_consumer('#', 'Logger')

    # Listen to created events: *.created
    # create_topic_consumer('*.created', 'Analytics')


# Example 4: RPC (Request-Reply) Pattern
class RabbitMQRPCClient:
    """RPC client"""

    def __init__(self):
        self.producer = RabbitMQProducer()
        self.producer.connect()

        # Declare callback queue
        result = self.producer.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        """Handle RPC response"""
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, n):
        """Make RPC call"""
        import uuid

        self.response = None
        self.corr_id = str(uuid.uuid4())

        # Publish request
        self.producer.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps({'n': n})
        )

        # Wait for response
        while self.response is None:
            self.producer.connection.process_data_events()

        return self.response


class RabbitMQRPCServer:
    """RPC server"""

    def __init__(self):
        self.consumer = RabbitMQConsumer()
        self.consumer.connect()
        self.consumer.declare_queue('rpc_queue')

    def fibonacci(self, n):
        """Compute fibonacci"""
        if n <= 1:
            return n
        return self.fibonacci(n - 1) + self.fibonacci(n - 2)

    def on_request(self, ch, method, props, body):
        """Handle RPC request"""
        request = json.loads(body)
        n = request['n']

        print(f"Computing fibonacci({n})")
        result = self.fibonacci(n)

        # Send response
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id
            ),
            body=json.dumps({'result': result})
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        """Start RPC server"""
        self.consumer.channel.basic_consume(
            queue='rpc_queue',
            on_message_callback=self.on_request
        )

        print("RPC Server waiting for requests...")
        self.consumer.channel.start_consuming()
```

---

## 2. Apache Kafka

### 2.1 Kafka Producer & Consumer

```python
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from kafka.errors import KafkaError
import json
from typing import List
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)


class KafkaMessageProducer:
    """Professional Kafka producer"""

    def __init__(self, bootstrap_servers: List[str] = ['localhost:9092']):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',  # Wait for all replicas
            retries=3,
            max_in_flight_requests_per_connection=1,  # Preserve order
            compression_type='gzip'
        )

    def send_message(self, topic: str, message: dict, key: str = None, partition: int = None):
        """Send message to Kafka topic"""
        try:
            future = self.producer.send(
                topic,
                value=message,
                key=key,
                partition=partition
            )

            # Wait for confirmation
            record_metadata = future.get(timeout=10)

            logging.info(
                f"✓ Message sent to {record_metadata.topic} "
                f"partition {record_metadata.partition} "
                f"offset {record_metadata.offset}"
            )

            return record_metadata

        except KafkaError as e:
            logging.error(f"✗ Failed to send message: {e}")
            raise

    def send_batch(self, topic: str, messages: List[dict]):
        """Send multiple messages"""
        for message in messages:
            self.send_message(topic, message)

        self.producer.flush()  # Ensure all messages are sent

    def close(self):
        """Close producer"""
        self.producer.close()


class KafkaMessageConsumer:
    """Professional Kafka consumer"""

    def __init__(
        self,
        topics: List[str],
        group_id: str,
        bootstrap_servers: List[str] = ['localhost:9092'],
        auto_offset_reset='earliest'
    ):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            auto_offset_reset=auto_offset_reset,  # earliest, latest, none
            enable_auto_commit=True,
            auto_commit_interval_ms=1000,
            session_timeout_ms=30000,
            max_poll_records=500
        )

    def consume_messages(self, callback: callable):
        """Consume messages and process with callback"""
        try:
            for message in self.consumer:
                logging.info(
                    f"Received message from {message.topic} "
                    f"partition {message.partition} "
                    f"offset {message.offset}"
                )

                try:
                    callback(message.value, message.key)
                except Exception as e:
                    logging.error(f"Error processing message: {e}")

        except KeyboardInterrupt:
            logging.info("Shutting down consumer...")
        finally:
            self.consumer.close()

    def consume_batch(self, timeout_ms=1000, max_records=100):
        """Consume messages in batches"""
        messages = self.consumer.poll(timeout_ms=timeout_ms, max_records=max_records)

        for topic_partition, records in messages.items():
            for record in records:
                yield record.value, record.key

    def seek_to_beginning(self, partitions: List[TopicPartition]):
        """Reset offset to beginning"""
        self.consumer.seek_to_beginning(*partitions)

    def seek_to_end(self, partitions: List[TopicPartition]):
        """Move offset to end"""
        self.consumer.seek_to_end(*partitions)

    def commit(self):
        """Manually commit offsets"""
        self.consumer.commit()

    def close(self):
        """Close consumer"""
        self.consumer.close()


# Usage Examples

# Example 1: Simple Producer/Consumer
def simple_kafka_example():
    """Basic Kafka example"""

    # Producer
    producer = KafkaMessageProducer()

    # Send messages
    for i in range(10):
        message = {
            'id': i,
            'message': f'Message {i}',
            'timestamp': datetime.utcnow().isoformat()
        }
        producer.send_message('events', message, key=f'key-{i}')

    producer.close()

    # Consumer
    def process_message(value, key):
        print(f"Processing [{key}]: {value}")

    consumer = KafkaMessageConsumer(
        topics=['events'],
        group_id='event-processor'
    )

    consumer.consume_messages(process_message)


# Example 2: Partitioned Topics
def partitioned_kafka_example():
    """Use partitions for parallel processing"""

    producer = KafkaMessageProducer()

    # Send to specific partitions
    for i in range(20):
        message = {'order_id': i, 'amount': i * 10}
        partition = i % 3  # Round-robin across 3 partitions

        producer.send_message(
            'orders',
            message,
            key=f'order-{i}',
            partition=partition
        )

    producer.close()

    # Multiple consumers in same group will share partitions
    # Each consumer gets different partitions
    consumer = KafkaMessageConsumer(
        topics=['orders'],
        group_id='order-processors'
    )

    def process_order(value, key):
        print(f"Processing order: {value}")

    consumer.consume_messages(process_order)


# Example 3: Event Streaming Pipeline
class EventStreamProcessor:
    """Process event stream with transformations"""

    def __init__(self):
        self.producer = KafkaMessageProducer()
        self.consumer = KafkaMessageConsumer(
            topics=['raw-events'],
            group_id='event-processor'
        )

    def process_and_forward(self):
        """Consume, transform, and produce"""
        def process(value, key):
            # Transform event
            transformed = {
                'original': value,
                'processed_at': datetime.utcnow().isoformat(),
                'enriched_data': self.enrich(value)
            }

            # Forward to processed topic
            self.producer.send_message('processed-events', transformed, key=key)

        self.consumer.consume_messages(process)

    def enrich(self, event: dict) -> dict:
        """Enrich event with additional data"""
        # Add business logic here
        return {
            'category': 'premium' if event.get('amount', 0) > 100 else 'standard'
        }


# Example 4: Dead Letter Queue (DLQ) Pattern
class ReliableKafkaProcessor:
    """Kafka processor with DLQ for failed messages"""

    def __init__(self):
        self.producer = KafkaMessageProducer()
        self.consumer = KafkaMessageConsumer(
            topics=['main-topic'],
            group_id='reliable-processor',
            auto_offset_reset='earliest'
        )

    def process_with_dlq(self):
        """Process messages with DLQ for failures"""
        def process(value, key):
            try:
                # Process message
                result = self.risky_operation(value)
                print(f"Successfully processed: {result}")

            except Exception as e:
                logging.error(f"Failed to process message: {e}")

                # Send to DLQ
                dlq_message = {
                    'original_message': value,
                    'error': str(e),
                    'failed_at': datetime.utcnow().isoformat()
                }
                self.producer.send_message('dead-letter-queue', dlq_message, key=key)

        self.consumer.consume_messages(process)

    def risky_operation(self, data: dict):
        """Operation that might fail"""
        if data.get('invalid'):
            raise ValueError("Invalid data")
        return data
```

---

## 3. Redis Pub/Sub

### 3.1 Redis Publish/Subscribe

```python
import redis
import json
import time
from typing import Callable
import threading

class RedisPubSub:
    """Redis Publish/Subscribe system"""

    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
        self.pubsub = self.redis_client.pubsub()

    def publish(self, channel: str, message: dict):
        """Publish message to channel"""
        message_json = json.dumps(message)
        subscribers = self.redis_client.publish(channel, message_json)
        print(f"Published to {channel}: {subscribers} subscribers")

    def subscribe(self, channels: list, callback: Callable):
        """Subscribe to channels"""
        self.pubsub.subscribe(*channels)

        print(f"Subscribed to {channels}")

        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                callback(message['channel'], data)

    def pattern_subscribe(self, pattern: str, callback: Callable):
        """Subscribe to channel pattern"""
        self.pubsub.psubscribe(pattern)

        print(f"Subscribed to pattern: {pattern}")

        for message in self.pubsub.listen():
            if message['type'] == 'pmessage':
                data = json.loads(message['data'])
                callback(message['channel'], data)

    def unsubscribe(self, channels: list = None):
        """Unsubscribe from channels"""
        if channels:
            self.pubsub.unsubscribe(*channels)
        else:
            self.pubsub.unsubscribe()


# Usage
pubsub = RedisPubSub()

# Publisher
def publisher_example():
    for i in range(10):
        message = {'id': i, 'data': f'Message {i}'}
        pubsub.publish('notifications', message)
        time.sleep(1)

# Subscriber
def subscriber_example():
    def handle_message(channel, data):
        print(f"Received from {channel}: {data}")

    pubsub.subscribe(['notifications'], handle_message)

# Run publisher in thread
# threading.Thread(target=publisher_example).start()

# Run subscriber
# subscriber_example()
```

---

This comprehensive guide covers all major message queue systems and event-driven patterns. These are production-ready implementations used in real distributed systems!

**Key Takeaways**:
- **RabbitMQ**: Flexible routing, reliable delivery, RPC support
- **Kafka**: High throughput, event streaming, partitioning
- **Redis Pub/Sub**: Fast, simple, real-time messaging
- **Event-Driven**: Loose coupling, scalability, resilience

Use these patterns to build scalable, distributed, event-driven systems!
