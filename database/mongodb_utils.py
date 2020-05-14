import logging

from motor.motor_asyncio import AsyncIOMotorClient
from .mongodb import db

from utils.get_env import mongo_url


async def connect_to_mongo():
    logging.info("connecting to mongo...")
    db.client = AsyncIOMotorClient(mongo_url,
                                   maxPoolSize=10,
                                   minPoolSize=10)
    # get a collection
    # Format db.<database_name>.<collection_name>
    # db.petDB = db.client.petDB.pet
    # logging.info("connected to petDB/pet")

    db.Telegram = db.client.telegram.auth
    logging.info("connected to telegram/auth")


async def close_mongo_connection():
    logging.info("closing connection...")
    db.client.close()
    logging.info("closed connection")
