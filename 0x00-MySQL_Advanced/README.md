# 0x00. MySQL advanced
**TABLE OF MATERIAL**
- [PASSWORD TO MYSQL](#password-to-mysql)
- [ADVANCED SQL](#advanced-sql)
	- [How to import a SQL dump](#how-to-import-a-sql-dump)
	- [TASK 0. We are all unique!](#0-we-are-all-unique)
	- [TASK 1. In and not out](#1-in-and-not-out)
	- [TASK 2. Best band ever!](#2-best-band-ever)
	- [TASK 3. Old school band](#3-old-school-band)
	- [TASK 4. Buy buy buy](#4-buy-buy-buy)
	- [TASK 5. Email validation to sent](#5-email-validation-to-sent)
	- [TASK 6. Add bonus](#6-add-bonus)
	- [TASK 7. Average score](#7-average-score)
	- [TASK 8. Optimize simple search](#8-optimize-simple-search)
	- [TASK 9. Optimize search and score](#9-optimize-search-and-score)
	- [TASK 10. Safe divide](#10-safe-divide)
	- [TASK 11. No table for a meeting](#11-no-table-for-a-meeting)
	- [TASK 12. Average weighted score](#12-average-weighted-score)
	- [TASK 13. Average weighted score for all!](#13-average-weighted-score-for-all)

## PASSWORD TO MYSQL
As I tried to work within the web-terminal (ALX sandbox). I faced a problem of authorization. I couldn't access the mysql because the root password was set and I had no knowledge of it.
The only solution was to reset it, and bellow are the steps to achieve that.
1. STOP THE MYSQL SERVER<br>
	To stop the mysql server write this command
	```bash
	sudo service mysql stop
	```
	If you are using *systemctl*
	```bash
	sudo systemctl stop mysql
	```
2. START MYSQL IN SAFE MODE<br>
	This is the command to start mysql in the safe mode
	```bash
	sudo mysqld_safe --skip-grant-tables &
	```
3. CONNECT TO MYSQL
	```bash
	mysql -u root
	```
	Now you have access to run queries.
4. UPDATE ROOT PASSWORD<br>
	Next we must update the password of the root, in order to prevent this problem from happening again.
	```sql
	FLUSH PRIVILEGES;
	ALTER USER 'root'@'localhost' IDENTIFIED BY 'pswd';
	```
	From now on our root password will be **pswd**
5. EXIT AND RESTART<br>
	Exit from mysql by running exit.
	```bash
	exit
	```
	Then run this to restart mysql service.
	```bash
	sudo service mysql restart
	```
6. TESTING<br>
	Test with a query.
	```bash
	echo "SHOW DATABASES" | mysql -uroot -p
	```

## ADVANCED SQL
During this project we are bound to learn the advanced features of the query language sql. The following README will be a step by step guide trough this project.
### How to import a SQL dump
In order for us to start the tasks of this project, we must import the SQL database that we will be using trough out. The steps to do that are mentioned in the section **MORE INFO** in the intranet. But if you are not able to follow there, here they are.
1. CREATE THE DATABASE
```bash
echo "CREATE DATABASE holberton;" | mysql -uroot -pecho "CREATE DATABASE holberton;" | mysql -uroot -p
```
2. DUMP INTO THE DATABASE
```bash
curl "https://s3.amazonaws.com/intranet-projects-files/holbertonschool-higher-level_programming+/274/hbtn_0d_tvshows.sql" -s | mysql -uroot -p holberton
```
	The option -s stands for silent.
1. TESTING
```bash
echo "SELECT * FROM tv_genres" | mysql -uroot -p holberton
```
You must get the following:
```
id  name
1   Drama
2   Mystery
3   Adventure
4   Fantasy
5   Comedy
6   Crime
7   Suspense
8   Thriller
```
We are now ready to work on them tasks.
### 0. We are all unique!
In this task we should write an SQL script that creates a table users following some requirements.
```sql
-- An SQL script that creates a table users.
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
email VARCHAR (255) NOT NULL UNIQUE,
name VARCHAR (255)
);
```
To test this we will follow the steps given by ALX, but we will change the database name to `holberton` since we imported it.
Run the following commands and notice the output.
```bash
echo "SELECT * FROM users;" | mysql -uroot -p holberton
```
This should return an `ERROR 1146` since the table `users` isn't yet created.
Now we shall test our script.
```bash
cat 0-uniq_users.sql | mysql -uroot -p holberton
```
If prompted with a password entry, use the password that we set earlier.
Next we will insert into the database `holberton`in the table `users` some lines.
```bash
echo 'INSERT INTO users (email, name) VALUES ("bob@dylan.com", "Bob");' | mysql -uroot -p holberton && echo 'INSERT INTO users (email, name) VALUES ("sylvie@dylan.com", "Sylvie");' | mysql -uroot -p holberton
```
We shall also test a duplicate entry.
```bash
echo 'INSERT INTO users (email, name) VALUES ("bob@dylan.com", "Jean");' | mysql -uroot -p holberton
```
This line should return `ERROR 1062` Duplicate entry.
Now we will display the content of the table `users`.
```bash
echo "SELECT * FROM users;" | mysql -uroot -p holberton
```
You should get the following:
```
id  email   name
1   bob@dylan.com   Bob
2   sylvie@dylan.com    Sylvie
```
### 1. In and not out
All we have to do in this task is to add another field to the table users.
```sql
-- An SQL script that creates a table users.
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
email VARCHAR (255) NOT NULL UNIQUE,
name VARCHAR (255),
country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);
```
The field `country` is choice between tree options. It shouldn't be Null and the default choice will be 'US' if no choice was given.
To test this, firstly run this command that will delete the table `users` from the database `holberton` in order to execute the new script.
```bash
echo "DROP TABLE users" | mysql -uroot -p holberton
```
Then run the script.
```bash
cat 1-country_users.sql | mysql -uroot -p holberton
```
Next we will insert some values in the table.
```bash
echo 'INSERT INTO users (email, name, country) VALUES ("bob@dylan.com", "Bob", "US");' | mysql -uroot -p holberton && echo 'INSERT INTO users (email, name, country) VALUES ("sylvie@dylan.com", "Sylvie", "CO");' | mysql -uroot -p holberton && echo 'INSERT INTO users (email, name) VALUES ("john@dylan.com", "John");' | mysql -uroot -p holberton
```
This should run seamlessly.
Next we will try to add a new line that contains a country that doesn't exist in the ENUM.
```bash
echo 'INSERT INTO users (email, name, country) VALUES ("jean@dylan.com", "Jean", "FR");' | mysql -uroot -p holberton
```
This should return and `ERROR 1265` Data truncated for column country.
Lastly check the content of table `users`.
```bash
echo "SELECT * FROM users;" | mysql -uroot -p holbertonecho "SELECT * FROM users;" | mysql -uroot -p holberton
```
You should receive the following:
```
id  email   name    country
1   bob@dylan.com   Bob US
2   sylvie@dylan.com    Sylvie  CO
3   john@dylan.com  John    US
```
### 2. Best band ever!
In this task we will be working with the same database, but we must import a new table that we were given.
Since I am working in the sandbox, i copied the file's content and saved it in a file inside the sandbox, gave the proper permissions, and run the file as follows.
```bash
cat bands.sql | mysql -uroot -p holberton
```
Run the following command to see what the table looks like.
```bash
echo "DESC metal_bands" | mysql -uroot -p holberton
```
And now it is time to write an sql script that ranks country origins of bands, ordered by the number of (non-unique) fans.
```sql
SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
```
This script will sum the number of fans per origin.
```bash
cat 2-fans.sql | mysql -uroot -p holberton
```
This is the output that you should get.
```
origin  nb_fans
USA 99349
Sweden  47169
Finland 32878
United Kingdom  32518
Germany 29486
Norway  22405
Canada  8874
The Netherlands 8819
Italy   7178
...
```
### 3. Old school band
Again in this task, same database, but our code has to work on any database. We shall create an SQL script that lists all the bands with the main style `Glam rock`, ranked by their longevity.
If we check the table's structure, using the query
```sql
DESC metal_bands
```
This is what we get:
```
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| id        | int(11)      | NO   | PRI | NULL    | auto_increment |
| band_name | varchar(255) | YES  |     | NULL    |                |
| fans      | int(11)      | YES  |     | NULL    |                |
| formed    | year(4)      | YES  |     | NULL    |                |
| origin    | varchar(255) | YES  |     | NULL    |                |
| split     | year(4)      | YES  |     | NULL    |                |
| style     | varchar(255) | YES  |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+
```
The fields that we will be working with are `band_name`, `formed` (The date in which the band has been formed), `split` (The date in which the band has been split), and `style` (The styles that the band perform).
The strategy we need to follow to solve this task is the following:
1. Select the band_name from the table metal_bands.
2. Get only the bands that has the style `Glam rock`.
3. Make sure the split field is not NULL, then subtract the forming date from the split date.
4. If the split date is NULL subtract the forming date from 2022.
5. Name the result of the subtraction `lifespan`.
6. Show results ordered by `lifespan` from the biggest to the smallest.
This is the query for me.
```sql
SELECT band_name,
CASE
	WHEN split IS NULL THEN 2022 - formed
	ELSE split - formed
END AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
```
This query has the condition placed before the FROM part.
The condition is grouped inside the CASE, END block. And the style has to be like `Glam rock`, since the style might contain 0 or more characters before it or after it, I added the wildcard `%`. Finally the results will be ordered by lifespan in an descending order.
Run the query.
```bash
cat 3-glam_rock.sql | mysql -uroot -p holberton
```
The result should be the following:
```
band_name   lifespan
Alice Cooper    56
Mötley Crüe   34
Marilyn Manson  31
The 69 Eyes 30
Hardcore Superstar  23
Nasty Idols 0
Hanoi Rocks 0
```
### 4. Buy buy buy
I am sure that that in this task we should create a new database, but I will be using the same database I used before.
We will be working with new tables.
```sql
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS orders;

CREATE TABLE IF NOT EXISTS items (
    name VARCHAR(255) NOT NULL,
    quantity int NOT NULL DEFAULT 10
);

CREATE TABLE IF NOT EXISTS orders (
    item_name VARCHAR(255) NOT NULL,
    number int NOT NULL
);

INSERT INTO items (name) VALUES ("apple"), ("pineapple"), ("pear");
```

```bash
cat 4-init.sql | mysql -uroot -p holberton
```
 Imagine you are shopping and took one 3 boxes of milk, the number of the boxes will decrease by 3 right? Well we want to achieve the same with these two tables, but we want this to be done automatically. This is where **Triggers**  comes in.

 > <mark>**TRIGGER** is a set of instructions that are executed automatically in response to an event. The instructions can be executed after or before the event. This propriety is very useful to enforce business rules, perform complex actions and more.</mark>

Now we want to create a trigger that performs decrease of quantity when ever an item is ordered. And it is okay if the quantity of items is negative.
```sql
CREATE TRIGGER decreaseQuantity
BEFORE INSERT ON orders
FOR EACH ROW
UPDATE items
SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;
```
- This is the query for me. We start by creating a trigger and giving it the name `decreaseQuantity`.
- The trigger will be triggered right before an insert on the table orders.
	<mark>For me it was better to do BEFORE than AFTER, because I imagined the case where the item's quantity is 0. Although we don't have to worry about that in this task.</mark>
- The trigger will be executed FOR EACH ROW. And let me explain that since it took me a while to understand.

	**In triggers we can use two types of operation levels.**
	1. FOR EACH ROW
			It is used when we want the trigger to be executed on each row. When using INSERT, UPDATE, or DELETE statements we can apply them on multiple rows. ex: `DELETE FROM fruit WHERE name = 'Apple';`. If we would create a trigger that updates the number of apples in the table fruit, we need to use FOR EACH ROW so that we can subtract the correct number of rows deleted.
	2. FOR EACH STATEMENT
		 For the same example above, using FOR EACH STATEMENT will cause us to subtract only one Apple from the table fruit despite if the query has caused the deletion of more than one Apple. Because in this case the trigger is executed for the whole statement regardless of the number of rows affected.
- The trigger will UPDATE the table items.
- It will subtract the number of items ordered from the item's quantity.
- The query will be executed on a specific item which is the one ordered.
```bash
cat 4-store.sql | mysql -uroot -p holberton
```
You have to test the trigger by adding orders and noticing what will happen to the items table.
```sql
SELECT * FROM items;
SELECT * FROM orders;

INSERT INTO orders (item_name, number) VALUES ('apple', 1);
INSERT INTO orders (item_name, number) VALUES ('apple', 3);
INSERT INTO orders (item_name, number) VALUES ('pear', 2);

SELECT "--";

SELECT * FROM items;
SELECT * FROM orders;
```
The above is the `4-main.sql` that we will be testing with.
```bash
cat 4-main.sql | mysql -uroot -p holberton
```
This is the expected output.
```
name    quantity
apple   10
pineapple   10
pear    10
--
--
name    quantity
apple   6
pineapple   10
pear    8
item_name   number
apple   1
apple   3
pear    2
```
### 5. Email validation to sent
Another one of them triggers! We will use a new table called `users`. We shall create a trigger that resets the attribute `valid_email` when ever the attribute `email` is updated.
```sql
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    id int not null AUTO_INCREMENT,
    email varchar(255) not null,
    name varchar(255),
    valid_email boolean not null default 0,
    PRIMARY KEY (id)
);

INSERT INTO users (email, name) VALUES ("bob@dylan.com", "Bob");
INSERT INTO users (email, name, valid_email) VALUES ("sylvie@dylan.com", "Sylvie", 1);
INSERT INTO users (email, name, valid_email) VALUES ("jeanne@dylan.com", "Jeanne", 1);
```
This is the table with the inserts. Execute its file.
```bash
cat 5-init.sql | mysql -uroot -p holberton
```
Time to create the trigger. Think, will we use FOR EACH ROW or FOR EACH STATEMENT?
The `valid_email` attribute is a boolean, resetting it meaning taking it back to its initial value which is 0. Keep in mind we should only reset it when the `email` attribute is updated.
```sql
CREATE TRIGGER resetAttribute
BEFORE UPDATE ON users
FOR EACH ROW
set NEW.valid_email = IF(NEW.email != OLD.email, 0, NEW.valid_email);
```
This is the trigger that I created. The trigger's name is `resetAttribute`, and it will be triggered when ever there is an update on the `email` in the table `users`, but only when the new email is different from the old email.
Test the trigger with this file.
```sql
SELECT * FROM users;

UPDATE users SET valid_email = 1 WHERE email = "bob@dylan.com";
UPDATE users SET email = "sylvie+new@dylan.com" WHERE email = "sylvie@dylan.com";
UPDATE users SET name = "Jannis" WHERE email = "jeanne@dylan.com";

SELECT "--";
SELECT * FROM users;

UPDATE users SET email = "bob@dylan.com" WHERE email = "bob@dylan.com";

SELECT "--";
SELECT * FROM users;
```

```bash
cat 5-main.sql | mysql -uroot -p holberton
```
This is the expected result:
```
id  email   name    valid_email
1   bob@dylan.com   Bob 0
2   sylvie@dylan.com    Sylvie  1
3   jeanne@dylan.com    Jeanne  1
--
--
id  email   name    valid_email
1   bob@dylan.com   Bob 1
2   sylvie+new@dylan.com    Sylvie  0
3   jeanne@dylan.com    Jannis  1
--
--
id  email   name    valid_email
1   bob@dylan.com   Bob 1
2   sylvie+new@dylan.com    Sylvie  0
3   jeanne@dylan.com    Jannis  1
```
### 6. Add bonus
In this task we shall create a stored procedure `AddBonus` that adds a new correction for a student. Me! I don't know what is a *stored procedure* to begin with, it is then time for me to find out.

> <mark>**Stored procedure**: Think of it like a function. It is a set of queries, statements that are grouped as one procedure. It is stored in the database and can be executed by a call.</mark>

We need *Stored procedures* as much as we need functions in programming languages. It has many advantages. This option allows **Reusability**, **Encapsulation**, **Parameter Passing** (we can pass parameters to a stored procedure), and many more.
In this task we will be using tree new tables, `users`, `projects`, and `corrections`.
This is the init:
```sql
DROP TABLE IF EXISTS corrections;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS projects;

CREATE TABLE IF NOT EXISTS users (
    id int not null AUTO_INCREMENT,
    name varchar(255) not null,
    average_score float default 0,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS projects (
    id int not null AUTO_INCREMENT,
    name varchar(255) not null,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS corrections (
    user_id int not null,
    project_id int not null,
    score int default 0,
    KEY `user_id` (`user_id`),
    KEY `project_id` (`project_id`),
    CONSTRAINT fk_user_id FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT fk_project_id FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE
);

INSERT INTO users (name) VALUES ("Bob");
SET @user_bob = LAST_INSERT_ID();

INSERT INTO users (name) VALUES ("Jeanne");
SET @user_jeanne = LAST_INSERT_ID();

INSERT INTO projects (name) VALUES ("C is fun");
SET @project_c = LAST_INSERT_ID();

INSERT INTO projects (name) VALUES ("Python is cool");
SET @project_py = LAST_INSERT_ID();


INSERT INTO corrections (user_id, project_id, score) VALUES (@user_bob, @project_c, 80);
INSERT INTO corrections (user_id, project_id, score) VALUES (@user_bob, @project_py, 96);
INSERT INTO corrections (user_id, project_id, score) VALUES (@user_jeanne, @project_c, 91);
INSERT INTO corrections (user_id, project_id, score) VALUES (@user_jeanne, @project_py, 73);
```
To explain these queries fast. The tables `users` and `projects` have primary keys that are used as foreign keys in the table `collection`, this last doesn't have a primary key instead its primary key is the combination of those foreign keys. That can be explicitly declared using `PRIMARY KEY ('user_id', 'project_id')`. This is what I think going on here.

Next we have a couple of inserts in `users` and `projects`, we store the returned the last automatically generated ID that was set as a result of the recent INSERT statement using `LAST_INSERT_ID()`.
Finally we will be using the ids we stored to store records in the table `correction`. What an amazing way to work. We stored the IDs of each insert and called them specific names, and then used them to insert in the table `correction` that uses both the ids of `users` and `projects` with giving the score for each record.
Run the script so that we can work with these tables.
```bash
cat 6-init.sql | mysql -uroot -p holberton
```
Now we need to create a stored procedure that adds a new correction for a student. We will be taking tree inputs (`user_id`,  `project_name`, and `score`) exactly the ones we used in the init, but this time we will use `project_name` instead of `project_id`, since we might need to include projects that already exist in the data base and not a new insert.
```sql
DELIMITER //
CREATE PROCEDURE AddBonus(IN userId INT, IN projectName VARCHAR(255), IN scoreProject INT)
BEGIN
	DECLARE projectId INT;
	SET projectId = (SELECT id from projects WHERE name = projectName);
	IF projectId IS NULL THEN
		INSERT INTO projects (name) VALUES (projectName);
		SET projectId = LAST_INSERT_ID();
	END IF;
	INSERT INTO corrections (user_id, project_id, score) VALUES (userId, projectId, scoreProject);
END //
DELIMITER ;
```
- We use DELIMITER because the sql takes the semicolon symbol `;` as an end of query, so in order to force it to ignore that we use DELIMITERS.
- A stored procedure's syntax is similar to functions in programming languages, inside of the parentheses we have the parameters that we will input, with their types.
- The BEGIN announces the beginning of the statements of the stored procedure.
- We declared a variable `projectId` as INT, where we will store the id of the project since we need it to insert into the table `corrections`.
- We give the variable the result of the SELECT query of the id where the name is equal to the given name. That way if the project already exists we will not recreate it, instead we will take its ID only.
- If the variable is NULL after this statement, we know that the project does not exist and we have to create it. And thus we INSERT a new project.
- We set the variable `projectId` to the ID of the last inserted row.
- All set, now we have the project Id and we can INSERT a new record in the `correction` table. We use for that the `user_id`,  the `project_id`, and the `score`.
Test your stored procedure with the following:
```sql
SELECT * FROM projects;
SELECT * FROM corrections;

SELECT "--";

CALL AddBonus((SELECT id FROM users WHERE name = "Jeanne"), "Python is cool", 100);
CALL AddBonus((SELECT id FROM users WHERE name = "Jeanne"), "Bonus project", 100);
CALL AddBonus((SELECT id FROM users WHERE name = "Bob"), "Bonus project", 10);
CALL AddBonus((SELECT id FROM users WHERE name = "Jeanne"), "New bonus", 90);

SELECT "--";

SELECT * FROM projects;
SELECT * FROM corrections;
```

```bash
cat 6-main.sql | mysql -uroot -p holberton
```
Notice the difference in output after calling the stored procedure, and how rows are added.
You should get the following.
```
id  name
1   C is fun
2   Python is cool
user_id project_id  score
1   1   80
1   2   96
2   1   91
2   2   73
--
--
--
--
id  name
1   C is fun
2   Python is cool
3   Bonus project
4   New bonus
user_id project_id  score
1   1   80
1   2   96
2   1   91
2   2   73
2   2   100
2   3   100
1   3   10
2   4   90
```
Keep in mind, the stored procedures and the triggers are stored for each database.
You can show a procedure with the following query.
```sql
SHOW CREATE PROCEDURE AddBonus;
```
And you can remove the stored procedure in case it did not work properly using the following query.
```sql
DROP PROCEDURE IF EXISTS AddBonus;
```
### 7. Average score
We know how to work we stored procedures, Now let's practice some more.
We shall create a stored procedure named `ComputeAverageScoreForUser`, that computes and store the average score for a student. The average score can be decimal. This time we are working with one input `user_id`.
We will use the same tables and same inserts as the task before.
```sql
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN userId INT)
BEGIN
	UPDATE users SET average_score = (
		SELECT AVG(score)
		FROM correction
		WHERE user_id = userId
	) WHERE id = userId;
END //
DELIMITER ;
```
The stored procedure has to update the row in the table user to add a column `average_score`, after it is queried to be extracted from the table corrections and calculated using `AVG`. The lookup is done using the input `userId`.
Execute the stored procedure:
```bash
cat 7-average_score.sql | mysql -uroot -p holberton
```
In order to test this stored procedure we can use the following main.
```sql
SELECT * FROM users;
SELECT * FROM corrections;

SELECT "--";
CALL ComputeAverageScoreForUser((SELECT id FROM users WHERE name = "Jeanne"));

SELECT "--";
SELECT * FROM users;
```
Run the script.
```bash
cat 7-main.sql | mysql -uroot -p holberton
```
Compare your results with the following.
```
id  name    average_score
1   Bob 0
2   Jeanne  0
user_id project_id  score
1   1   80
1   2   96
2   1   91
2   2   73
--
--
--
--
id  name    average_score
1   Bob 0
2   Jeanne  82
```
### 8. Optimize simple search
In this task we are required to create an index `idx_name_first` on the table `names` and the first letter of `name`.
You may wonder what are indexes? and why do we need to use them?

> <mark>Indexes are data structures that allow efficient retrieval of data based on a column for example. Think of an index section of a book and how it provides quick reference to where an information is.
We need the indexing because it helps retrieve data quickly and instead of spending time executing a query, indexes can be used as a reference...</mark>

But as the task said, "Index is not the solution for any performance issue, but well used, it’s really powerful!".
In order to work on this task we need to import a table from the file they gave us, it is a file that contains a table called `names`, in which we inserted values. Now we must create an index on the first letter of the name.
```sql
CREATE INDEX idx_name_first ON names (name(1));
```
This is how we create an index on the table names, the first character.
Test this in the following way.
Start by executing the file to create the table we will use for testing.
```bash
cat names.sql | mysql -uroot -p holberton
```
Now we will test a normal search query without using the index.
```bash
mysql -uroot -p holberton
```
This is the query we will use.
```sql
SELECT COUNT(name) FROM names WHERE name LIKE 'a%';
```
You shall get this result:
```
+-------------+
| COUNT(name) |
+-------------+
|      302936 |
+-------------+
```
Now, exit the mysql and run the file that contains our index query.
```bash
cat 8-index_my_names.sql | mysql -uroot -p holberton
```
In order to see the created index we can run the following command:
```bash
echo "SELECT COUNT(name) FROM names WHERE name LIKE 'a%';" | mysql -uroot -p holberton
```
You will get the same previous output but notice the execution time.
### 9. Optimize search and score
The next task requires the same thing as the task before, but this time we are creating an index on both the first character of the name in the table names and the score.
It goes the same way and it is not complicated.
```sql
CREATE INDEX idx_name_first_score ON names (name(1), score);
```
Before you execute your query, let's test a search query on this huge table to see how fast will the results show.
```bash
echo "
SELECT COUNT(name) FROM names WHERE name LIKE 'a%' AND score < 80;" | mysql -uroot -p holberton
```
You will get the following result.
```
+-------------+
| count(name) |
+-------------+
|       60717 |
+-------------+
```
Now let's execute our index query.
```bash
cat 9-index_name_score.sql | mysql -uroot -p holberton
```
In order to see the index you created, you can use the following:
```bash
echo "SELECT COUNT(name) FROM names WHERE name LIKE 'a%' AND score < 80;" | mysql -uroot -p holberton
```
You will get the same result as before but you have to notice the execution time.
### 10. Safe divide
In this task we shall create a function that returns the first number divided by the second number or 0 if the second number is equal to zero. Keep in mind a and b must be integers.
```sql
DELIMITER //
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT
BEGIN
IF (b = 0) THEN RETURN 0;
ELSE RETURN a / b;
END IF;
END //
DELIMITER ;
```
The function takes a and b, and we define that it returns float. If b is equal to zero we return 0. Else we return the division of a / b.
In order to test what we created we shall create a new table numbers.
```sql
DROP TABLE IF EXISTS numbers;

CREATE TABLE IF NOT EXISTS numbers (
    a int default 0,
    b int default 0
);

INSERT INTO numbers (a, b) VALUES (10, 2);
INSERT INTO numbers (a, b) VALUES (4, 5);
INSERT INTO numbers (a, b) VALUES (2, 3);
INSERT INTO numbers (a, b) VALUES (6, 3);
INSERT INTO numbers (a, b) VALUES (7, 0);
INSERT INTO numbers (a, b) VALUES (6, 8);
```
Execute the file.
```bash
cat 10-init.sql | mysql -uroot -p holberton
```
Then we shall execute the file of our function.
```bash
cat 10-div.sql | mysql -uroot -p holberton
```
Let's test what we created. We shall use a normal query, and then use our function, then compare the results to see if it works as expected.
```bash
echo "SELECT (a / b) FROM numbers;" | mysql -uroot -p holberton
```
You will get the following results.
```
(a / b)
5.0000
0.8000
0.6667
2.0000
NULL
0.7500
```
And now we shall use our function.
```bash
echo "SELECT SafeDiv(a, b) FROM numbers;" | mysql -uroot -p
```
With the function we set, we will get the following result.
```
SafeDiv(a, b)
5
0.800000011920929
0.6666666865348816
2
0
0.75
```
We already set the result to be returned as a float, so in cases where the number has no number after the comma it will be shown as int, else it is shown as a float.
### 11. No table for a meeting
The last task in our mandatory tasks. We need to create a view `need_meeting` that lists all students that have a score under 80, and no `last_meeting` or more than 1 month.
```sql
DROP VIEW IF EXISTS need_meeting;
CREATE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80
AND (last_meeting IS NULL
OR DATEDIFF(CURDATE(), last_meeting) > 30);
```
This script created the view `need_meeting`. We used a condition to get only the students with the score under 80, and the `last_meeting` is either null or less than one month.
In order to test the script we will initialize the table students.
```sql
DROP TABLE IF EXISTS students;

CREATE TABLE IF NOT EXISTS students (
    name VARCHAR(255) NOT NULL,
    score INT default 0,
    last_meeting DATE NULL
);

INSERT INTO students (name, score) VALUES ("Bob", 80);
INSERT INTO students (name, score) VALUES ("Sylvia", 120);
INSERT INTO students (name, score) VALUES ("Jean", 60);
INSERT INTO students (name, score) VALUES ("Steeve", 50);
INSERT INTO students (name, score) VALUES ("Camilia", 80);
INSERT INTO students (name, score) VALUES ("Alexa", 130);DROP TABLE IF EXISTS students;

CREATE TABLE IF NOT EXISTS students (
    name VARCHAR(255) NOT NULL,
    score INT default 0,
    last_meeting DATE NULL
);

INSERT INTO students (name, score) VALUES ("Bob", 80);
INSERT INTO students (name, score) VALUES ("Sylvia", 120);
INSERT INTO students (name, score) VALUES ("Jean", 60);
INSERT INTO students (name, score) VALUES ("Steeve", 50);
INSERT INTO students (name, score) VALUES ("Camilia", 80);
INSERT INTO students (name, score) VALUES ("Alexa", 130);
```
Run the script as follows:
```bash
cat 11-init.sql | mysql -uroot -p holberton
```
Then we use the following main to test with.
```sql
SELECT * FROM need_meeting;
SELECT "--";
UPDATE students SET score = 40 WHERE name = 'Bob';
SELECT * FROM need_meeting;
SELECT "--";
UPDATE students SET score = 80 WHERE name = 'Steeve';
SELECT * FROM need_meeting;
SELECT "--";
UPDATE students SET last_meeting = CURDATE() WHERE name = 'Jean';
SELECT * FROM need_meeting;
SELECT "--";
UPDATE students SET last_meeting = ADDDATE(CURDATE(), INTERVAL -2 MONTH) WHERE name = 'Jean';
SELECT * FROM need_meeting;
SELECT "--";
SHOW CREATE TABLE need_meeting;
SELECT "--";
SHOW CREATE TABLE students;
```
Run the main.
```bash
cat 11-main.sql | mysql -uroot -p holberton
```
Check the validity of the output.
```
name
Jean
Steeve
--
--
name
Bob
Jean
Steeve
--
--
name
Bob
Jean
--
--
name
Bob
--
--
name
Bob
Jean
--
--
View    Create View character_set_client    collation_connection
XXXXXX<yes, here it will display the View SQL statement :-) >XXXXXX
--
--
Table   Create Table
students    CREATE TABLE `students` (\n  `name` varchar(255) NOT NULL,\n  `score` int(11) DEFAULT '0',\n  `last_meeting` date DEFAULT NULL\n) ENGINE=InnoDB DEFAULT CHARSET=latin1
```
### 12. Average weighted score
The first of our advanced tasks, and we shall write an SQL script that creates a stored procedure `ComputeAverageWeightedScoreForUser`, it computes the average score for a student using the user_id input.
```sql
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN userId INT)
BEGIN
	SET @userScores := (
	SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
	FROM corrections
	JOIN projects ON corrections.project_id = projects.id
	WHERE corrections.user_id = userId);
	UPDATE users SET average_score = @userScores WHERE id = userId;
END //
DELIMITER ;
```
The procedure takes `userId` as input, I stored the result that will be added to the field `average_score` in `@userScores`.
The query to calculate the average score is multiplying the `corrections.score` with `projects.weight` divide it on the `SUM(projects.weight)`. How will we get to use both of these tables the simple way? We use JOIN.

The JOIN might seam scary, but here is a link for you to always find the syntax of any query, JOIN is also among those. [MYSQL CHEAT SHEET](https://devhints.io/mysql).
The query i used is `SELECT ... FROM t1 JOIN t2 ON t1.id1 = t2.id2 WHERE condition;`.
The final step will be to update the users table by setting the new column `average_score = @usersScore` for the `userId`.
Lets test our procedure. Firstly run the procedure.
```bash
cat 100-average_weighted_score.sql | mysql -uroot -p holberton
```
We will be testing with the following:
```sql
SELECT * FROM users;
SELECT * FROM projects;
SELECT * FROM corrections;

CALL ComputeAverageWeightedScoreForUser((SELECT id FROM users WHERE name = "Jeanne"));

SELECT "--";
SELECT * FROM users;
```

```bash
cat 100-main.sql | mysql -uroot -p holberton
```
You shall get the following results.
```
id  name    average_score
1   Bob 0
2   Jeanne  82
id  name    weight
1   C is fun    1
2   Python is cool  2
user_id project_id  score
1   1   80
1   2   96
2   1   91
2   2   73
--
--
id  name    average_score
1   Bob 0
2   Jeanne  79
```
### 13. Average weighted score for all!
The last task is about a script that creates a stored procedure `ComputeAverageWeightedScoreForUsers`That computes that average weighted score for all students.It is basically the same as the task before, but this time we are not taking any input, since we will be giving scores for all the students stored.
```sql
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
		UPDATE users SET average_score = (
			SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
			FROM corrections
			JOIN projects ON corrections.project_id = projects.id
			WHERE corrections.user_id = users.id);
END //
DELIMITER ;
```
The idea here is to update each user with the calculated value of the average score. By using update before hand, we are minimizing the code since we can get the id of each user that way.
I used the same equation as before. We can use JOIN as we did in the task before.

The final step is to make sure that the `correction.user_id` is the same as the `users.id` that we got from the update query.
Now we will use the same tables `users`, `projects`, `corrections` as before. We can now run the procedure.
```bash
cat 101-average_weighted_score.sql | mysql -uroot -p holberton
```
To test we will use this file.
```sql
SELECT * FROM users;
SELECT * FROM projects;
SELECT * FROM corrections;

CALL ComputeAverageWeightedScoreForUsers();

SELECT "--";
SELECT * FROM users;
```

```bash
cat 101-main.sql | mysql -uroot -p holberton
```
You shall get the following output.
```
id  name    average_score
1   Bob 0
2   Jeanne  0
id  name    weight
1   C is fun    1
2   Python is cool  2
user_id project_id  score
1   1   80
1   2   96
2   1   91
2   2   73
--
--
id  name    average_score
1   Bob 90.6667
2   Jeanne  79
```
