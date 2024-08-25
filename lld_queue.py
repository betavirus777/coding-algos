'''Components of the Distributed Queue
Producers:
  - Components that send messages to the queue.
  - They should be able to publish messages to a specific topic.
  - Producers can send messages with keys for partitioning.

Consumers:
  - Components that consume messages from the queue.
  - Consumers subscribe to one or more topics and receive messages in the order they were produced.
  - They can consume messages from specific partitions of a topic.

Brokers:
  - Servers that store the messages and manage the queue.
  - They handle receiving messages from producers and delivering them to consumers.
  - Brokers manage multiple topics and partitions.

Topics:
  - A logical channel to which producers send messages and from which consumers read messages.
  - Each topic is divided into multiple partitions, enabling parallel processing.

Partitions: 
  - A division of a topic. Each partition is an ordered sequence of messages.
  - Partitions are distributed across different brokers to ensure scalability and fault tolerance.
  - Each partition can have a leader broker, which handles all read and write requests for that partition.

Zookeeper (or a similar coordination service):
  -  Manages the distributed state of the system.
  - Handles leader election for partitions, tracks consumer offsets, and stores metadata.


Each message in a partition has an offset, which is its position in the partition.
Consumers use offsets to track which messages they have already processed.'''

import threading
from queue import Queue
from collections import defaultdict

class Broker:
    def __init__(self, broker_id):
        self.broker_id = broker_id
        self.topics = defaultdict(lambda: defaultdict(Queue))  # {topic: {partition: Queue}}
        self.partitions = defaultdict(int)  # Tracks number of partitions per topic

    def create_topic(self, topic_name, num_partitions):
        self.partitions[topic_name] = num_partitions
        for partition in range(num_partitions):
            self.topics[topic_name][partition] = Queue()

    def produce(self, topic_name, partition, message):
        self.topics[topic_name][partition].put(message)
        print(f"Broker {self.broker_id}: Produced message to {topic_name} partition {partition}")

    def consume(self, topic_name, partition):
        message = self.topics[topic_name][partition].get()
        print(f"Broker {self.broker_id}: Consumed message from {topic_name} partition {partition}")
        return message

class Producer:
    def __init__(self, broker):
        self.broker = broker

    def send(self, topic_name, key, message):
        partition = key % self.broker.partitions[topic_name]
        self.broker.produce(topic_name, partition, message)

class Consumer:
    def __init__(self, broker):
        self.broker = broker

    def receive(self, topic_name, partition):
        return self.broker.consume(topic_name, partition)

# Example usage:
broker = Broker(broker_id=1)
broker.create_topic("test_topic", 3)

producer = Producer(broker)
consumer = Consumer(broker)

# Producing messages
producer.send("test_topic", key=0, message="Hello, World!")
producer.send("test_topic", key=1, message="Another message")

# Consuming messages
consumer.receive("test_topic", partition=0)
consumer.receive("test_topic", partition=1)
