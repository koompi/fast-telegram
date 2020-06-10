from fastapi import HTTPException
from ..db.mongodb_validators import validate_object_id


def fix_data_id(data):
    if data.get("_id", False):
        # change ObjectID to string
        data["_id"] = str(data["_id"])
        return data
    else:
        raise ValueError(
            f"No `_id` found! Unable to fix data ID for data: {data}"
        )


async def _get_data_or_404(conn, id: str, database, collection):
    _id = validate_object_id(id)
    data = await conn[database][collection].find_one({"_id": _id})
    if data:
        return fix_data_id(data)
    else:
        raise HTTPException(
            status_code=404, 
            detail="data not found or Invalid Id"
            )
