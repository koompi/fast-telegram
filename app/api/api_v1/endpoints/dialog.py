from fastapi import APIRouter, Depends, HTTPException

from ....core.jwt import get_current_user_authorizer
from ....db.mongodb import AsyncIOMotorClient, get_database

from ....models.user import User
from ....models.dialog import DialogInInput
from ....utils.telegram.dialog import get_all_dialogs


router = APIRouter()


@router.post(
    '/get_dialogs',
    # response_model=ChannelInResponse,
    tags=['dialogs'],
    status_code=200
)
async def get_dialogs(
    dialog: DialogInInput,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=401,
            detail='unauthorize user'
        )

    res = await get_all_dialogs(user.telegram_auth_key, dialog)
    return res


