# Anime Store
My portfolio project. Anime store in Django

![image](https://user-images.githubusercontent.com/77948380/139658682-7bb4ab50-fda7-4e0a-a65b-ad28dfdb6196.png)

## Development
### System dependencies
* python 3.8
* Django 3.2.8
* psycopg2-binary 2.9.1
* environs 9.3.4
* Pillow 8.4.0

### Setup environment
* Rename .env.dist to <b>.env</b>
* Fill in your <b>data</b>
* <code>SECRET_KEY</code> is needed to secure sessions on the client side
* <code>PG_NAME</code> - database name
* <code>PG_HOST</code> is responsible for where your database is located
* <code>PG_USER and PG_PASSWORD</code> are needed to access the database


### Launch
* <code>git clone https://github.com/waydk/anime_store</code>
* <code>cd anime_store</code>
* If you don't have poetry <code>pip install poetry</code>
* Install dependencies: <code>poetry install</code>
* Activate the virtual environment <code>poetry shell</code>
* Creating migrations <code>python manage.py makemigrations store</code>
* Migration <code>python manage.py migrate</code>
* Creating a superuser <code>python manage.py createsuperuser</code>
* Launching an application <code>python manage.py runserver</code>
