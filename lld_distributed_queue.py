import threading
from queue import Queue
from collections import defaultdict
import time

class Broker:
    def __init__(self, broker_id):
        self.broker_id = broker_id
        self.topics = defaultdict(lambda: defaultdict(Queue))  # {topic: {partition: Queue}}
        self.partitions = defaultdict(int)  # Tracks number of partitions per topic
        self.consumer_groups = defaultdict(lambda: defaultdict(list))  # {topic: {group_id: [consumers]}}

    def create_topic(self, topic_name, num_partitions):
        self.partitions[topic_name] = num_partitions
        for partition in range(num_partitions):
            self.topics[topic_name][partition] = Queue()

    def produce(self, topic_name, partition, message):
        self.topics[topic_name][partition].put(message)
        print(f"Broker {self.broker_id}: Produced message to {topic_name} partition {partition}")

    def subscribe(self, consumer, topic_name, group_id):
        self.consumer_groups[topic_name][group_id].append(consumer)

    def distribute_messages(self, topic_name):
        num_partitions = self.partitions[topic_name]
        while True:
            for partition in range(num_partitions):
                if not self.topics[topic_name][partition].empty():
                    message = self.topics[topic_name][partition].get()
                    group_id = partition % len(self.consumer_groups[topic_name])
                    consumers = self.consumer_groups[topic_name][group_id]
                    consumer = consumers[partition % len(consumers)]
                    threading.Thread(target=consumer.consume_message, args=(message,)).start()

            time.sleep(1)  # Prevents tight loop, simulates real-time processing

class Producer:
    def __init__(self, broker):
        self.broker = broker

    def send(self, topic_name, key, message):
        partition = key % self.broker.partitions[topic_name]
        self.broker.produce(topic_name, partition, message)

class Consumer:
    def __init__(self, name):
        self.name = name

    def consume_message(self, message):
        print(f"{self.name} consumed message: {message}")
        # Simulate message processing time
        time.sleep(0.5)

class ConsumerGroup:
    def __init__(self, broker, topic_name, group_id):
        self.broker = broker
        self.topic_name = topic_name
        self.group_id = group_id

    def subscribe(self, consumer):
        self.broker.subscribe(consumer, self.topic_name, self.group_id)

# Example usage:
broker = Broker(broker_id=1)
broker.create_topic("test_topic", 3)

producer = Producer(broker)

# Create consumers and consumer groups
consumer1 = Consumer("Consumer 1")
consumer2 = Consumer("Consumer 2")
consumer3 = Consumer("Consumer 3")
consumer4 = Consumer("Consumer 4")

group1 = ConsumerGroup(broker, "test_topic", group_id=0)
group1.subscribe(consumer1)
group1.subscribe(consumer2)

group2 = ConsumerGroup(broker, "test_topic", group_id=1)
group2.subscribe(consumer3)
group2.subscribe(consumer4)

# Start the message distribution in a separate thread
threading.Thread(target=broker.distribute_messages, args=("test_topic",)).start()

# Producing messages
producer.send("test_topic", key=0, message="Message 1")
producer.send("test_topic", key=1, message="Message 2")
producer.send("test_topic", key=2, message="Message 3")
producer.send("test_topic", key=3, message="Message 4")
producer.send("test_topic", key=4, message="Message 5")

# The system will keep running and processing messages
