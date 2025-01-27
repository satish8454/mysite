# Python Chat Application

This project is real-time chat application which built using django and daphne for socket communication.

## Prerequisites

In order to run the python script, your system must have the following programs/packages installed
* Python 3.x

## steps to 

### step 1 : clone the project
```
git clone https://github.com/satish8454/mysite.git
```
### step 2 : open cmd and change the directory to /mysite

### step 3 : create virual environment and activate it
on windows
```
pip install pipenv
pipenv shell
```
on ubuntu
```
sudo pip3 install virtualenv 
virtualenv venv
source venv/bin/activate
```
### step 3 : install the reuirements
```
pip install -r requirements.txt
```
### step 4 : make migrations in database
```
python manage.py makemigrations
python manage.py migrate
```
### step 5 : run the server
```
python manage.py runserver
```

If server runs successfully below will reflect on bash
Starting ASGI/Daphne version 4.1.2 development server at http://127.0.0.1:8000/
