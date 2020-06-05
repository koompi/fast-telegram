import logging
from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import (
    MONGODB_URL,
    MAX_CONNECTIONS_COUNT,
    MIN_CONNECTIONS_COUNT
) 
from .mongodb import db


async def connect_to_mongo():
    logging.info('connecting to mongodb...')
    db.client = AsyncIOMotorClient(
        (str(MONGODB_URL)),
        maxPoolSize=MAX_CONNECTIONS_COUNT,
        minPoolSize=MIN_CONNECTIONS_COUNT
    )
    logging.info('connecting to mongodb/db！')


async def close_mongo_connection():
    logging.info('closing connection...')
    db.client.close()
    logging.info('closed connection!')
