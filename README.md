# Excalibur

**meetings.txt** (notes from meetings with "customer")

## Setup

- install [postgresql](https://github.com/PaceMakr/teamexcalibur/blob/prototype/install-postgresql.md)</br>
- create a postgres user name:`super_user` with password `password`
- create a database named: `little_bytes_development`
- install [python3.6](https://www.python.org/downloads/) **optional: use a virtualenv(https://virtualenv.pypa.io/en/stable/installation/) for the project** 
- clone this repository:
	- create a folder where you want to save this project
	- cd into the folder from the command line
	- run `git clone -b prototype https://github.com/PaceMakr/teamexcalibur`
- open a terminal and cd into the projects repository and run `pip install -r requirements.txt`
- cd into school_app/ **use ls to make sure there is a manage.py file in your directory**
- run `python manage.py migrate`
- create an admin account:
	- run `python manage.py createsuperuser`
	- enter `admin`
	- any email
	- the password `littlebytes`
- run `python manage.py runserver`
- open a browser and go to [localhost:8000/admin](localhost:8000/admin)

Finally log in with `admin` and `littlebytes` as the credentials
