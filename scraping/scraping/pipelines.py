import ujson
import sys

from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError

class KafkaPipeline:
    '''
        Pushes a serialized item to Kafka topic
    '''
    def __init__(self, producer, topic_prefix, use_base64) -> None:
        self.producer = producer
        self.topic_prefix = topic_prefix
        self.use_base64 = use_base64

    @classmethod
    def from_settings(cls, settings):
        print(settings)
        try:
            producer = KafkaProducer(
                bootstrap_servers=settings['KAFKA_HOSTS'],
                retries=3,
                linger_ms=settings['KAFKA_PRODUCER_BATCH_LINGER_MS'],
                buffer_memory=settings['KAFKA_PRODUCER_BUFFER_BYTES'],
                value_serializer=lambda v: ujson.dumps(v).encode('utf-8')
            )
        except Exception as e:
            print(e)
            sys.exit(1)
        topic_prefix = settings['KAFKA_TOPIC_PREFIX']
        use_base64 = settings['KAFKA_BASE_64_ENCODE']
        return cls(producer, topic_prefix, use_base64)
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)
    
    def _kafka_success(self, item, spider, response):
        '''
            Callback for successful send
        '''
        print('Sent to kafka')
        print(item)

    def _kafka_failure(self, item, spider, response):
        '''
            Callback for failer send
        '''
        print('Failed to send to kafka')
        print(item)

    def process_item(self, item, spider):
        try:
            topic = f'{self.topic_prefix}.scraped_firehose'
            datum = dict(item)
            future = self.producer.send(topic, datum)
            future.add_callback(self._kafka_success, datum, spider)
            future.add_errback(self._kafka_failure, datum, spider)

        except KafkaTimeoutError:
            print('Caught KafkaTimeoutException')
        
        return item

    def close_spider(self, spider):
        self.producer.flush()
        self.producer.close(timeout=10)