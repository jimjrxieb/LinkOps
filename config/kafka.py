"""
Kafka configuration and connection management
"""

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
import logging
from typing import Dict, Any

from config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class KafkaManager:
    """Kafka connection manager"""
    
    def __init__(self):
        self.producer = None
        self.consumer = None
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS.split(',')
    
    def get_producer(self) -> KafkaProducer:
        """Get or create Kafka producer"""
        if self.producer is None:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                retries=3,
                acks='all'
            )
        return self.producer
    
    def get_consumer(self, topic: str, group_id: str = None) -> KafkaConsumer:
        """Get or create Kafka consumer"""
        if group_id is None:
            group_id = settings.KAFKA_CONSUMER_GROUP
            
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            auto_commit_interval_ms=1000
        )
        return self.consumer
    
    def send_message(self, topic: str, message: Dict[str, Any], key: str = None) -> bool:
        """Send message to Kafka topic"""
        try:
            producer = self.get_producer()
            future = producer.send(topic, value=message, key=key)
            record_metadata = future.get(timeout=10)
            logger.info(f"Message sent to {topic} partition {record_metadata.partition}")
            return True
        except KafkaError as e:
            logger.error(f"Failed to send message to Kafka: {e}")
            return False
    
    def close(self):
        """Close Kafka connections"""
        if self.producer:
            self.producer.close()
        if self.consumer:
            self.consumer.close()


# Global Kafka manager instance
kafka_manager = KafkaManager()


def get_kafka_manager() -> KafkaManager:
    """Get Kafka manager instance"""
    return kafka_manager
