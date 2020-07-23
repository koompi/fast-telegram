import os
from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret
from databases import DatabaseURL


API_V1_STR = '/api'
JWT_TOKEN_PREFIX = 'jwt'
ACCESS_TOKEN_EXPIRE_MINUTES = 10080

load_dotenv('.env')

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')


MAX_CONNECTIONS_COUNT = int(os.getenv('MAX_CONNECTIONS_COUNT', 10))
MIN_CONNECTIONS_COUNT = int(os.getenv('MIN_CONNECTIONS_COUNT', 10))

SECRET_KEY = Secret(os.getenv('SECRET_KEY', 'secret key for project'))
SALT = os.getenv('SALT', 'SALT for token')
ALGORITHM = os.getenv('ALGORITHM', 'ALGORITHM for hash')

PROJECT_NAME = os.getenv('PROJECT_NAME', 'FastAPI application with Telegram')

ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv('ALLOWED_HOSTS', ''))
MONGODB_URL = os.getenv('MONGODB_URL', '')
MONGODB_URL = DatabaseURL(MONGODB_URL)

users_collection_name = 'users'
server_token_collection_name = 'server_token'
upload_collection_name = 'upload'
channel_collection_name = 'channel'
database_name = 'TELEGRAM_DB'

parse_mode = 'html'

sticker_dir = "./documents/stickers/"
image_type = "jpg"
gif_dir = "./documents/gifs/"
git_type = "gif"
voice_type = "ogg"
voice_dir = "./documents/voices/"
audio_type = "mpeg"
audio_dir = "./documents/audios/"
video_type = "mp4"
video_dir = "./documents/videos/"
image_dir = "./documents/images/"
file_dir = "./documents/files/"
profile_dir = "./documents/profiles/"
