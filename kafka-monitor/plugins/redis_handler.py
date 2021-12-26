import redis
import settings
from .base_handler import BaseHandler

class RedisHandler(BaseHandler):
    schema = "redis_schema.json"
    
    def setup(self):
        '''
            Setup redis connection
        '''
        print('Connecting to redis')
        self.redis_conn = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
        print('Connected to redis')

    def handle(self, dict):
        '''
            Process a valid message from kafka
        '''
        print('Adding message to redis set')
        # Get id of the instance that sent this message
        scraper_instance_id = dict['instance_id']
        for crypto_name in ['BTC', 'ETH']:
            score = dict['timestamp']
            value = dict['crypto_count'][crypto_name]
            # zadd updates element if key already exists
            # so if two different scraper instance send message at same timestamp
            # only one of them will be in the set, but we want both
            # therefor 'key' is combination of both 'value' and scraper instance if
            self.redis_conn.zadd(f'{settings.REDIS_SORTED_SET_NAME}_{crypto_name}', {
                    f'{value}_{scraper_instance_id}': score
                },
            )
        print('Message added to redis sorted set')

    