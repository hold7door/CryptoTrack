import logging
import aioredis

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseSettings

class Config(BaseSettings):
    # The default URL expects the app to run in a docker container
    redis_url: str = 'redis://localhost:6379'


log = logging.getLogger(__name__)
config = Config()
redis = aioredis.from_url(config.redis_url, decode_responses=True)
app = FastAPI(title='CryptoTrack API server')


""" async def initialize_redis():
   
    log.info('Connected to redis')
 """
@app.get('/daily')
async def get_daily():
    result = await redis.zrangebyscore('crypto_daily_BTC', '-inf', 'inf')
    print(result)
    return {
        'result': result
    }
    
""" 
@app.on_event('startup')
async def startup_event():
    await initialize_redis() """