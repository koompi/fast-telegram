from ..models.token import ServerTokenBase
from ..db.mongodb import AsyncIOMotorClient
from ..core.config import database_name, server_token_collection_name
from .get_by_id import _get_data_or_404


async def create_server_token(
    conn: AsyncIOMotorClient,
    token_doc: ServerTokenBase
) -> ServerTokenBase:
    server_token = token_doc.dict()

    await conn[database_name][server_token_collection_name]\
        .insert_one(server_token)

    return ServerTokenBase(**server_token)


async def get_token_by_id(
    conn: AsyncIOMotorClient,
    id: str
):
    token = await _get_data_or_404(id)
    return token


async def fetch_all_servertoken(
    conn: AsyncIOMotorClient
):
    tokens = []
    rows = conn[database_name][server_token_collection_name].find()
    async for row in rows:
        token = {
            '_id': str(row['_id']),
            'server_token': row['server_token'],
            'created_by': row['created_by'],
            'created_at': row['created_at'],
        }
        tokens.append(token)
    return tokens
