# Catalog - Got It Final Project

A project at the end onbroading process for Software Engineer Backend Intern at Got It. 
The application provides user registration and authentication system, as well as the ability to manage a collection of categories and the corresponding items.
To have a deeper understanding of Catalog, please have a look at the [PROJECT DESIGN](https://docs.google.com/document/d/1aUUa2PIvmPsqalHUqkqyqfr6UV8thWDOE_tWJnKriz4/edit). <br>
The project's teck stack: Python, Flask, RESTful API, Flask-SQLALchemy, MySQL.


## Installation 
#### 1. Prerequisites
- Python 3.0 or later is required. If you haven't installed it, please visit https://www.python.org/downloads/. (version 3.8.6 is recommended since it was used during the development process).
- <code>pip</code> (package installer for Python). Follow the instructions in https://pypi.org/project/pip/ to get the lastest version.

#### 2. Download the project
- This could be easily down via download button on GitHub or you can use <code>git clone</code> if you prefer.

#### 3. Setting up a virtual environment
To avoid environmental conflicts, let's set up a virtual environment to run the application
- Download the virtualenv package:
> $ pip install virtualenv 
- Now direct to the root folder of Catalog, creat a new virtual environment with specific python version (here I use python 3.8). You can also change the name of the environment if you want (here I set its name is <code>venv</code>).
> $ virtualenv venv --python=python3.8
- Now activate the environment:
> $ source venv/bin/activate 

#### 4. Installing third-party libraries
All the required packages have been listed in <code>requirements.txt</code>. In the terminal, run the following command to install them:
> $ pip install -r requirements.txt
>
Some of the main packages you might want to have a look at:
- [Flask](https://flask.palletsprojects.com/en/1.1.x/): Mircro web framework
- [Flask-SQLALchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/): Object-raltional mapping (ORM)
- [pyJWT](https://pyjwt.readthedocs.io/en/latest/): Encoding and decoding the JSON Web Token. 
- [marshmallow](https://marshmallow.readthedocs.io/en/stable/): Validating request data
- [flask-hashing](https://flask-hashing.readthedocs.io/en/latest/): Hashing user's password
- [pytest](https://docs.pytest.org/en/stable/): Testing the application 

#### 5. Setting up SQL server
- In Mac OS, turn on MySQL Server in **System Preferences**. Now we need to create 2 database **catalog** and **catalog_test** for *development* environment and *testing* environment respectively. This can be done by logging in to the MySQL server, then open a WorkBench Query Tab and execute the following statement:
> CREATE DATABASE catalog;
>
> CREATE DATABASE catalog_test;

- All the tables will be automatically generated when we first run the application, thus we don't have to do it manually. However, you will need to tell the application the URI of your SQL server. To do this, look for the <code>config.py</code> file, set the <code>SQLALCHEMY_DATABASE_URI</code> attribute of both development environment and testing enviroment equal to the password of your SQL server:
> SQLALCHEMY_DATABASE_URI = 'mysql://root:<your_password>@localhost/catalog'
>
> SQLALCHEMY_DATABASE_URI = 'mysql://root:<your_password>@localhost/catalog_test'

- For example:
> SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/catalog'
>
> SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/catalog_test'

#### 6. Some configuration
In <code>config</code> folder, you can change these following configuration: 
- <code>SECRET_KEY</code>: secret key used for authorization system. 
- <code>JWT_EXPIRATION_PERIOD</code>: the length of expiration period of JWT access token.

## Setting up a local host web server
- From the terminal, we need to change the default environment (production) to development mode:
> $ export FLASK_ENV=development
- Then, simply run:
> $ python run.py
- The application is now available at local host: <code>http://127.0.0.1:5000</code>.

## Testing
- [Postman](https://www.postman.com): You can use postman to create custom requests to our local host.
- [Pytest](https://docs.pytest.org/en/stable/): I wrote several tests in the <code>tests</code> folder. You can write some test by your own, there are functions in <code>helpers.py</code> may help you simplify the work. But first, let's switch to testing environment:
> $ export FLASK_ENV=testing

- After that, run this command to obtain the testing results:
> $ pytest --cov
