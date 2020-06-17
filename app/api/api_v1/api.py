from fastapi import APIRouter

from .endpoints.authenticaion import router as auth_router
from .endpoints.user import router as user_router
from .endpoints.key_generate import router as gen_key
from .endpoints.upload_dowload import router as udload
from .endpoints.chat_channel import router as cha

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(gen_key)
router.include_router(udload)
router.include_router(cha)
