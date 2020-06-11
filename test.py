from datetime import datetime, timedelta
import jwt

JWT_SECRET = '123456'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 60


# payload = {
#         'decrypt key': 'test key',
#         'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
#     }


# jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

jwt_token = b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZSI6Iis4NTU4ODI3NzgzMDkiLCJleHAiOjE1OTI0NTk1MDEsInN1YiI6ImFjY2VzcyJ9.dRIVAEwTzFWZ0n_1Kh4cUWdpHOio0Iv4Y6as8-rZxZE"

try:
    decoded = jwt.decode(jwt_token, JWT_SECRET, JWT_ALGORITHM)
    print(decoded)
except jwt.exceptions.ExpiredSignatureError as e:
    print(e)
except jwt.exceptions.InvalidSignatureError as e:
    print(e)

#  b"uvicorn app.main:app --reload"
