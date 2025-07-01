"""
Shared Kafka Configuration
Kafka producer and consumer management for LinkOps microservices
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "kafka:9092").split(",")
KAFKA_TOPIC_PREFIX = os.getenv("KAFKA_TOPIC_PREFIX", "linkops")


class KafkaManager:
    """Manages Kafka producer and consumer connections"""

    def __init__(self):
        self.producer = None
        self.consumers = {}

    def get_producer(self) -> KafkaProducer:
        """Get or create Kafka producer"""
        if self.producer is None:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=KAFKA_BROKERS,
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                    key_serializer=lambda k: k.encode("utf-8") if k else None,
                    retries=3,
                    acks="all",
                )
                logger.info("Kafka producer initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Kafka producer: {str(e)}")
                raise
        return self.producer

    def get_consumer(self, topic: str, group_id: str) -> KafkaConsumer:
        """Get or create Kafka consumer for topic"""
        consumer_key = f"{topic}_{group_id}"

        if consumer_key not in self.consumers:
            try:
                consumer = KafkaConsumer(
                    topic,
                    bootstrap_servers=KAFKA_BROKERS,
                    group_id=group_id,
                    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                    key_deserializer=lambda k: k.decode("utf-8") if k else None,
                    auto_offset_reset="earliest",
                    enable_auto_commit=True,
                    auto_commit_interval_ms=1000,
                )
                self.consumers[consumer_key] = consumer
                logger.info(f"Kafka consumer initialized for topic: {topic}")
            except Exception as e:
                logger.error(
                    f"Failed to initialize Kafka consumer for {topic}: {str(e)}"
                )
                raise

        return self.consumers[consumer_key]

    def send_message(
        self, topic: str, message: Dict[str, Any], key: Optional[str] = None
    ) -> bool:
        """Send message to Kafka topic"""
        try:
            producer = self.get_producer()
            future = producer.send(topic, value=message, key=key)
            record_metadata = future.get(timeout=10)

            logger.info(
                f"Message sent to {topic} partition {record_metadata.partition} offset {record_metadata.offset}"
            )
            return True

        except KafkaError as e:
            logger.error(f"Failed to send message to {topic}: {str(e)}")
            return False

    def close(self):
        """Close all Kafka connections"""
        if self.producer:
            self.producer.close()
            self.producer = None

        for consumer in self.consumers.values():
            consumer.close()
        self.consumers.clear()

        logger.info("Kafka connections closed")


# Global Kafka manager instance
kafka_manager = KafkaManager()


def get_kafka_producer() -> KafkaProducer:
    """Get Kafka producer instance"""
    return kafka_manager.get_producer()


def get_kafka_consumer(topic: str, group_id: str) -> KafkaConsumer:
    """Get Kafka consumer instance"""
    return kafka_manager.get_consumer(topic, group_id)


def send_kafka_message(
    topic: str, message: Dict[str, Any], key: Optional[str] = None
) -> bool:
    """Send message to Kafka topic"""
    return kafka_manager.send_message(topic, message, key)


def close_kafka_connections():
    """Close all Kafka connections"""
    kafka_manager.close()
