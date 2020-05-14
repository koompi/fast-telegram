from database.mongodb_validators import validate_object_id
from fastapi import HTTPException
from database.mongodb import db


def fix_telegram_id(telegram):
    if telegram.get("_id", False):
        # change ObjectID to string
        telegram["_id"] = str(telegram["_id"])
        return telegram
    else:
        raise ValueError(
            f"No `_id` found! Unable to fix telegram ID for telegram: {telegram}"
        )

# Get telegram Function.


async def _get_telegram_or_404(id: str):
    _id = validate_object_id(id)
    telegram = await db.Telegram.find_one({"_id": _id})
    if telegram:
        return fix_telegram_id(telegram)
    else:
        raise HTTPException(status_code=404, detail="telegram not found")
