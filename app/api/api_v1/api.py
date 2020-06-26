from fastapi import APIRouter

from .endpoints.authenticaion import router as auth_router
from .endpoints.user import router as user_router
from .endpoints.key_generate import router as genkey_router
from .endpoints.upload_dowload import router as udload_router
from .endpoints.chat_channel import router as cha_router
from .endpoints.stream import router as str_router
from .endpoints.dialog import router as dialog_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(genkey_router)
router.include_router(udload_router)
router.include_router(cha_router)
router.include_router(str_router)
router.include_router(dialog_router)
