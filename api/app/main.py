import logging
import aioredis

from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseSettings, BaseModel

from datetime import datetime, timedelta

class Config(BaseSettings):
    # The default URL expects the app to run in a docker container
    redis_url: str = 'redis://localhost:6379'

class Query(BaseModel):
    time_range: str


log = logging.getLogger(__name__)
config = Config()
redis = aioredis.from_url(config.redis_url, decode_responses=True)

app = FastAPI(title='CryptoTrack API server')


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


""" async def initialize_redis():
   
    log.info('Connected to redis')
 """
@app.post('/daily')
async def get_daily(query: Query):
    print(query)
    time_range = query.time_range
    
    timestamps = []

    if time_range == '7d':
        now = datetime.now()
        delta_day = timedelta(1)
        delta_sec = timedelta(0, 1)
        for _ in range(7):
            current_timestamp = datetime.timestamp(now)
            prev_date = now - delta_day
            prev_timestamp = datetime.timestamp(prev_date)
            timestamps.append((prev_timestamp, current_timestamp))
            now = prev_date - delta_sec

    print(timestamps)

    result = {
        'BTC': [],
        'ETH': []
    }

    for crypto in ['BTC', 'ETH']:
        for mn, mx in timestamps:
            values = await redis.zrangebyscore(f'crypto_daily_{crypto}', mn, mx)
            sm = 0
            for value in values:
                sm += int(value.split('-')[0])
            result[crypto].append(sm)

    return {
        'result': result
    }
    
""" 
@app.on_event('startup')
async def startup_event():
    await initialize_redis() """