 Installing PostgreSQL Server

[Postgres](https://www.postgresql.org/) is a widely used and open source relational database. The applications we are developing in this program make use of postgres, so it is important that we make sure it is installed.


## Installing on a Mac (with Homebrew)

The easiest way to install postgres on the Mac is using Homebrew with the following commands:

```
brew update
brew install postgresql
```

### Starting up the server

After installing postgres, you need to turn it on before you can begin using it. There are a few ways to do that, but the easiest is using the homebrew services manager. You can set that up as follows:

First, install brew services if you don't already have it installed:

```
brew tap homebrew/services
```

Next, you can start, stop, or restart the postgres server with the following commands:

For starting it up:

```
brew services start postgresql
```

For stopping the server:

```
brew services stop postgresql
```

To restart the server run:

```
brew services restart postgresql
```


## Installing on Ubuntu 16.04

On Ubuntu 16.04 you can install postgres with the following commands:

```
$ sudo apt-get update
$ sudo apt-get install -y postgresql-9.5 postgresql-server-dev-9.5
```

### Create your DB user

On Ubuntu, you will have to make a postgresql user that matches your Ubuntu username.


Run these commands **once** (replace `UBUNTU_USERNAME` with your own username):

```
sudo su - postgres
createuser -P -s -e USERNAME
exit
```

**remember the username and password you set as it will be used for database connections**</br>

> After this one time step, you wont need the sudo commands to create more databases and database users.


### `createdb`

Each project will need a separate database. You can create the database as follows:

```
$ createdb -h localhost -U db_username MYAPPNAME_development
```

> This command creates a database named `MYAPPNAME_development` that is owned by `db_username` and can only be accessed via `localhost`

- You should change `MYAPPNAME` to your project name
- It is good practice to add `_development` or `_production` so that we know if the database contains dev data or customer data.
- You will need the database _name_, _username_, and _password_ to connect your apps to the database.
