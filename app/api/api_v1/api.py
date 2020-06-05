from fastapi import APIRouter

from .endpoints.authenticaion import router as auth_router
from .endpoints.user import router as user_router
from .endpoints.key_generate import router as gen_key

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(gen_key)
