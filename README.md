## Welcome to Fast-Telegram

Hi i`m very novice at programing. So my code not so perfect i will try hard to make it more clear and
easy to watch if have any problem with this please ask me anytime.



### To Use Sent Mail In Telegram

Create Telegram Api_Hash and Api_Id :
  - [Login] to your Telegram account
   with the phone number of the developer account to use.
 - Click under API Development tools.
 - A Create new application window will appear. Fill in your application details.
  There is no  need to enter any URL, and only the first two fields (App title and Short name)
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
		- MAX_CONNECTIONS_COUNT=15
		- MIN_CONNECTIONS_COUNT=10
		- PROJECT_NAME = Fast-Telegram
		- SECRET_KEY =  ' your very secret key '
		- SALT = 'similar to secret key ' 
		- ALGORITHM = 'HS256'   
		- ALLOWED_HOSTS='"127.0.0.1", "localhost"'
```sh
 $ pipenv install -r requirements.txt (install module that we need for this project)
 $ uvicorn main:app --reload (use to run fast api app )
```
- And go to [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) 
	* To look into all route in api

#### API Route Detail

- About [http://127.0.0.1:8000/api/users](http://127.0.0.1:8000/api/users)
	* This route use create account (use must already telegram account)  
		```sh
		HTTP Methods POST
		```
	*  |  Parameter | Requirent | DataType | Default|Detail |
	    | ------ | ------ | ------ | ------ | ------ |
	    | email | True | String ||your email Account | 
	    | phone | True | String ||your phone number that register to telegram | 
	    | password | True | String ||your password| 
	    | force_sms | False | Bool |False |use to send sms to your phone number| 

- About [http://127.0.0.1:8000/api/confirm](http://127.0.0.1:8000/api/confirm)
	* This route use to confirm your telegram account 
	* Require Authentication
	  ```sh
		HTTP Methods POST
	  ```
	* |  Parameter | Requirent | DataType | Default|Detail |
	    | ------ | ------ | ------ | ------ | ------ |
	    | code | True | Integer ||code that send to your telegram  | 

- About [http://127.0.0.1:8000/api/resend](http://127.0.0.1:8000/api/resend)
	* This route use to resend telegram confirm code
	* Require Authentication
	  ```sh
		HTTP Methods GET
	  ```

- About [http://127.0.0.1:8000/api/users/login](http://127.0.0.1:8000/api/users/login)
	* This route use to login to account
	  ```sh
		HTTP Methods POST
	  ```
	* |  Parameter | Requirent | DataType | Default|Detail |
	    | ------ | ------ | ------ | ------ | ------ |
	    | email | True | String ||your email Account | 
	    | password | True | String ||your password| 

- About [http://127.0.0.1:8000/api/generate_key](http://127.0.0.1:8000/api/generate_key)
	* This route use to generate new public and private key to encrypt decrypt file (Admin and uploader)
	*  Require Authentication
		 ```sh
		  HTTP Methods POST
		 ```
	* |  Parameter | Requirent | DataType | Default|Detail |
	    | ------ | ------ | ------ | ------ | ------ |
	    | password | False | String ||use to make your private key more secure| 
	    | force_gen | False | Bool | Fasle|use when you already have public and private key| 
	
- About [http://127.0.0.1:8000/api/generate_token](http://127.0.0.1:8000/api/generate_token)
	* This route use to generate new sever token to create shared key that can open
	 with encrypt file with admin private key or user private key (admin only)
	*  Require Authentication
		 ```sh
		  HTTP Methods GET
		 ```

- About [http://127.0.0.1:8000/api/create_channel](http://127.0.0.1:8000/api/create_channel)
	* This route use to to create channel 
	*  Require Authentication
		 ```sh
		  HTTP Methods POST
		 ```
	* |  Parameter | Requirent | DataType | Default|Detail |
	    | ------ | ------ | ------ | ------ | ------ |
	    | channel_name | True | String ||your channel name you want to create| 
	    | about | True | String | |detail about your channel| 
	    | megagroup | False | Boolen | False |If It is Trur became channel with limit member| 
	    | address | False | String | None |your address| 
	    | lat | False | Float | None |your  Latitude| 
	    | long | False | Float | None |your Longitude| 

- About [http://127.0.0.1:8000/api/assign_uploader](http://127.0.0.1:8000/api/assign_uploader)
- About [http://127.0.0.1:8000/api/change_channel_permission](http://127.0.0.1:8000/api/change_channel_permission)
	* This 2 route use same parameter one for change user permission and one for assign new uploader
	*  Require Authentication
		 ```sh
		  HTTP Methods POST
		 ``
	* |  Parameter | Requirent | DataType | Default|Detail |
	    | ------ | ------ | ------ | ------ | ------ |
	    | channel | True | String ||your channel invite link or channel id| 
	    | user | True | String | |username or user id| 
	    | post_messages | False | Boolen | True |member can post messages| 
	    | delete_messages | False | Boolen | None |member can delete messages | 
	    | pin_messages | False | Boolen | None |member can pin messages| 
	    | edit_messages | False | Boolen | None |member can edit messages| 
	    | invite_users | False | Boolen | None |member can invite new member| 
	    | change_info | False | Boolen | None |member can change channel info| 
	    | ban_users | False | Boolen | None |member can ban other member| 
	  
- About [http://127.0.0.1:8000/api/change_channel_type](http://127.0.0.1:8000/api/change_channel_type)
	* This route use to change private channel to pubilc channel not support change public channel to private
	*  Require Authentication
		 ```sh
		  HTTP Methods POST
		 ```
	* |  Parameter | Requirent | DataType | Default|Detail |
	    | ------ | ------ | ------ | ------ | ------ |
	    | channel_id | True | String ||your channel invite link or channel id| 
	    | channel_name | True | String | |pubilc channel name| 

- About [http://127.0.0.1:8000/api/upload_files](http://127.0.0.1:8000/api/upload_files)
	* This route use to upload encrypt file to telegram (Admin and uploader)
	*  Require Authentication
		 ```sh
		  HTTP Methods POST
		 ```
	* |  Parameter | Requirent | DataType | Default|Detail |
	    | ------ | ------ | ------ | ------ | ------ |
	    | filename | True | String ||your file location in your device| 
	    | channel |True  | String | |channel invite link | 
	    | token_id |True  | String | |id of server token that admin generate | 
	    | password |False  | String | |your private key password if you use password when generate key |

- About [http://127.0.0.1:8000/api/streaming](http://127.0.0.1:8000/api/streaming)
	* This route use to stream decrypt file  frome telegram (Admin and uploader)
	*  Require Authentication
		 ```sh
		  HTTP Methods POST
		 ```
	* #### Admin
	* |  Parameter | Requirent | DataType | Default|Detail |
	    | ------ | ------ | ------ | ------ | ------ |
	    | file_id | True | String ||file id that you want to get| 
	    | channel |True  | String | |channel invite link | 
	    | password |False | String | |your private key password if you use password when generate key |
	    
	    * #### Uploader
	* |  Parameter | Requirent | DataType | Default|Detail |
	    | ------ | ------ | ------ | ------ | ------ |
	    | file_id | True | String || file id that you want to get| 
	    | channel |True  | String | |channel invite link | 
	    | token_id |True  | String | |id of server token that admin generate | 
	    | password |False | String | |your private key password if you use password when generate key |
		* #### User
	* |  Parameter | Requirent | DataType | Default|Detail |
	    | ------ | ------ | ------ | ------ | ------ |
	    | file_id | True | String ||file id that you want to get| 
	    | channel |True  | String | |channel invite link | 
	    | secret_key |True | String | |your key that you buy |
  
 - About [http://127.0.0.1:8000/api/buy_course](http://127.0.0.1:8000/api/buy_course)
	* This route use to buy key
	*  Require Authentication
	  ```sh
		HTTP Methods POST
	  ```
	* |  Parameter | Requirent | DataType | Default|Detail |
	    | ------ | ------ | ------ | ------ | ------ |
	    | file_id | True | String ||file id that you want to buy| 
	    | expire | False | Integer | 7|how long your key avalible| 



[Login]: <https://my.telegram.org/auth>
[watch]: <https://www.youtube.com/watch?v=D-NYmDWiFjU>
[Telegram]: <https://docs.telethon.dev/en/latest/basic/signing-in.html>
