## Welcome to Fast-Telegram

Hi i`m very novice at programing. So my code not so perfect i will try hard to make it more clear and
easy to watch if have any problem with this please ask me anytime.

### To Use Sent Mail In Telegram

Create Telegram Api_Hash and Api_Id :

- [Login] to your Telegram account
  with the phone number of the developer account to use.
- Click under API Development tools.
- A Create new application window will appear. Fill in your application details.
  There is no need to enter any URL, and only the first two fields (App title and Short name)
  can currently be changed later.
- Click on Create application at the end. Remember that your API hash is secret and Telegram
  won’t let you revoke it. Don’t post it anywhere!

> More detail [Telegram] Api

## To Run This Python Code

Install the dependencies and create env filw

- First create .env file
  - example
    - API_ID = API_ID = xxxxxxx
    - API_HASH = 'xxxxxxxxxxxxxxxxxxxxxx'
    - MONGO_URL = '{Your Mongo db url}'

```sh
 $ pipenv install -r requirements.txt (install module that we need for this project)
 $ uvicorn main:app --reload (use to run fast api app )
```

- And go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

[login]: https://my.telegram.org/auth
[watch]: https://www.youtube.com/watch?v=D-NYmDWiFjU
[telegram]: https://docs.telethon.dev/en/latest/basic/signing-in.html
