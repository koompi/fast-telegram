from fastapi import Depends, FastAPI, Header, HTTPException
from database.mongodb_utils import close_mongo_connection, connect_to_mongo
from telegram_auth.routes import telegramAuth_router
from telegram_dialogs.routes import telegramDialogs_router

app = FastAPI(
    title="Telegram API",
    description="Telegram API Documentation",
    version="1.0.0",)


app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


app.include_router(
    telegramAuth_router,
    prefix="/telegram auth",
    tags=["telegram auth"],
    responses={404: {"description": "Not found"}},
)


app.include_router(
    telegramDialogs_router,
    prefix="/telegram dialogs",
    tags=["telegram dialogs"],
    responses={404: {"description": "Not found"}},
)

# uvicorn main:app --reload
# 5ea28612fc329b4980f45c39
