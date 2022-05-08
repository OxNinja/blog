# Setup your database with Docker


Yeah, I wanted to do one of those for a long time 😁

So, we have to stay at home for the moment, I decided to make a "walkthrough" about something I used sometimes and I couldn't remember all the commands. So, **let's build our MySQL database** within a **Docker container** 🐳 !

## Get the Docker image

I will be using the `mysql` image from the [Docker hub](https://hub.docker.com/_/mysql).

```shell
docker pull mysql
```

## Run the container

For further details, you can read the official documentation for the image on Docker hub. I will just go through the basic steps I use.

```shell
docker run --name my_container -e MYSQL_ROOT_PASSWORD=toor -d mysql:latest
```

* `--name` : setup a name for our container
* `-e` : setup environment variables
	* `MYSQL_ROOT_PASSWORD` : need explainations ?
* `-d` : run in deamon mode
* `mysql:latest` : use the `mysql` image in the latest version

## Administrate the database

Once the container is running in background, we have to connect to it :

```shell
docker exec -it my_container /bin/bash
```

Here, we connect to the running container and pop a shell in interactive mode. We have to connect to the database :

```shell
mysql -uroot -ptoor
```

Now we can start to use SQL commands for our database.

### Create the database

```sql
CREATE DATABASE my_db;
USE my_db
```

### Create the table

```sql
CREATE TABLE compotes (id INT, name TEXT, note INT);
```

### Manipulate the table

#### INSERT

We want now to add some data in our table :

```sql
INSERT INTO compotes (id, name, note) VALUES (0, "Apple", 3);
INSERT INTO compotes (id, name, note) VALUES (1, "Apple & banana", 5), (2, "Apple & pear", 4), (3, "Apple & apple", 3);
```

#### UPDATE

Oh no, I f'cked up my data ! Apple & banana is not that tasty !

```sql
UPDATE compotes SET (note=4) WHERE id=1;
```

Better.

#### DELETE

So drunk I added apple & apple in my table *sight*

```sql
DELETE FROM compotes WHERE name="Apple & apple";
```

OK, we are good.

#### SELECT

I want to see my beautiful compotes now !

```sql
SELECT * FROM compotes;

SELECT name, note FROM compotes;

SELECT * FROM compotes WHERE id > 1 AND note = 3;
```

## Use SQL script

We don't want to re-type all the database when building a new container !

SQL scripts are cool for that : 

```sql
# populate.sql
# SQL script to build the compotes table in our database

create database my_db;
use my_db

create table compotes(id int,
	name text,
	note int);

insert into compotes(id, text, note) values
	(0, "Apple", 3),
	(1, "Apple & banana", 5),
	(2, "Apple & pear", 4);
```

And execute the script on the running container :

```shell
docker exec -i my_container sh -c 'exec mysql -uroot -ptoor' < populate.sql
```

