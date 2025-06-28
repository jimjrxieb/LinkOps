# Kafka Configuration - DISABLED
# This file has been disabled to simplify the LinkOps Core stack.
# Kafka functionality can be re-enabled by uncommenting this file and
# updating imports.

# from kafka import KafkaProducer, KafkaConsumer
# from kafka.errors import KafkaError
# import json
# import logging
# from typing import Dict, Any, Optional
# from config.settings import settings

# class KafkaManager:
#     """Kafka manager for LinkOps Core"""
#
#     def __init__(self):
#         self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS.split(',')
#         self.producer = None
#         self.consumer = None
#         self.logger = logging.getLogger(__name__)
#
#     def get_producer(self) -> KafkaProducer:
#         """Get or create Kafka producer"""
#         if self.producer is None:
#             self.producer = KafkaProducer(
#                 bootstrap_servers=self.bootstrap_servers,
#                 value_serializer=lambda v: json.dumps(v).encode('utf-8'),
#                 key_serializer=lambda k: k.encode('utf-8') if k else None
#             )
#         return self.producer
#
#     def get_consumer(self, topic: str, group_id: str = None) -> KafkaConsumer:
#         """Get or create Kafka consumer"""
#         if group_id is None:
#             group_id = settings.KAFKA_CONSUMER_GROUP
#
#         self.consumer = KafkaConsumer(
#             topic,
#             bootstrap_servers=self.bootstrap_servers,
#             group_id=group_id,
#             auto_offset_reset='earliest',
#             enable_auto_commit=True,
#             value_deserializer=lambda x: json.loads(x.decode('utf-8'))
#         )
#         return self.consumer
#
#     def send_message(self, topic: str, message: Dict[str, Any], key: str = None) -> bool:
#         """Send message to Kafka topic"""
#         try:
#             producer = self.get_producer()
#             future = producer.send(topic, value=message, key=key)
#             record_metadata = future.get(timeout=10)
#             self.logger.info(f"Message sent to {topic} partition {record_metadata.partition} offset {record_metadata.offset}")
#             return True
#         except KafkaError as e:
#             self.logger.error(f"Failed to send message to Kafka: {e}")
#             return False
#
#     def close(self):
#         """Close Kafka connections"""
#         if self.producer:
#             self.producer.close()
#         if self.consumer:
#             self.consumer.close()

# # Global Kafka manager instance
# kafka_manager = KafkaManager()

# def get_kafka_manager() -> KafkaManager:
#     """Get Kafka manager instance"""
#     return kafka_manager
