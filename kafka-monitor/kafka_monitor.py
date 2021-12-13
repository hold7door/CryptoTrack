from kafka import KafkaConsumer
import uuid
import ujson
import time

import settings

class KafkaMonitor:

    consumer = None
    
    def __init__(self):
        self.my_uuid = str(uuid.uuid4()).split('-')[4]
    
    def _create_consumer(self):
        '''
            Tries establishing the Kafka consumer connection
        '''
        try:
            """Tries establishing the kafka consumer connection"""
            brokers = settings.KAFKA_HOSTS
            print(f'Creating new kafka consumer using brokers {str(brokers)} and topic ${settings.KAFKA_INCOMING_TOPIC}')
            return KafkaConsumer(
                settings.KAFKA_INCOMING_TOPIC,
                group_id=settings.KAFKA_GROUP,
                bootstrap_servers=brokers,
                consumer_timeout_ms=settings.KAFKA_CONSUMER_TIMEOUT,
                auto_offset_reset=settings.KAFKA_CONSUMER_AUTO_OFFSET_RESET,
                auto_commit_interval_ms=settings.KAFKA_CONSUMER_COMMIT_INTERVAL_MS,
                enable_auto_commit=settings.KAFKA_CONSUMER_AUTO_COMMIT_ENABLE,
            )
        except KeyError as e:
            print('Missing setting name')
            print(str(e))
        except:
            print("Couldn't initialize kafka consumer for topic")
            raise

    def _process_messages(self):
        # print("processing messages")
        try:
            for message in self.consumer:
                if message is not None:
                    loaded_dict = ujson.loads(message.value)
                    print(loaded_dict)
        except:
            self.consumer.seek_to_end()

    def _main_loop(self):
        while True:
            self._process_messages()
            time.sleep(settings.SLEEP_TIME)

    def _setup_kafka(self):
        '''
            Setup kafka connections
        '''
        self.consumer= self._create_consumer()

    def run(self):
        '''
            Setup and run
        '''
        self._setup_kafka()
        self._main_loop()


def main():
    kafka_monitor = KafkaMonitor()
    kafka_monitor.run()

if __name__ == '__main__':
    main()