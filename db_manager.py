import sqlite3


# for testing only
import os
os.remove("./blogdata.db")


DB_FILE = "blogdata.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()


# creates the tables
def createTables():

    # command to create the table of all users.
    # Columns:
    # username (str)
    # password (str)
    # unique id (int primary key)
    command = "CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);"

    # command to create the table of all blogs.
    # Columns:
    # user id (int)
    # username (str)
    # blog title (str)
    # blog id (int primary key)
    # date created (str)
    # blog bio (str)
    command += "CREATE TABLE IF NOT EXISTS blogs(user_id INT, username TEXT, blog_title TEXT, blog_id INTEGER PRIMARY KEY AUTOINCREMENT, date_created TEXT, blog_bio TEXT);"

    # command to create table of all blog entries.
    # Columns:
    # blog id (int)
    # username (str)
    # entry id (int primary key)
    # entry title (str)
    # entry content (str)
    # date created (str)
    command += "CREATE TABLE IF NOT EXISTS entries(blog_id INT, username TEXT, entry_id INTEGER PRIMARY KEY AUTOINCREMENT, entry_title TEXT, entry_content TEXT, date_created TEXT);"

    # executes the command and commits the change
    c.executescript(command)
    db.commit()


# returns the username and password for a given user_id in a tuple (username,
# password)
# consider case when 2 users have the same username and password. Technically
# would work because they have different ids. Should we make username unique as well?
def getUserId(username: str) -> int:
    command = 'SELECT id FROM users WHERE username = "{}";'.format(
        username)
    for row in c.execute(command):
        info = row

    return info[0]


# returns (username, password, user_id) for a given username. Returns None
# if argument username is not present in the database
def getUserInfo(username: str):
    command = 'SELECT username, password, id FROM users WHERE username = "{}";'.format(
        username)
    info = ()
    for row in c.execute(command):
        info += (row[0], row[1], row[2])
    if info == ():
        return None
    return info


# returns a tuple in the following format: (login_successful, issue, user_id)
# login_successful will be either True (correct info) or False
# issue will be None if login_successful is True. Otherwise will be "user not found" or
# "incorrect username or password"
# user_id will be returned if login_successful. None if not login_successful
def checkLogin(username: str, password: str) -> tuple:
    info = getUserInfo(username)
    if info == None:
        return (False, "User not found", None)
    elif (info[0] == username) and (info[1] == password):
        return (True, None, info[2])
    return (False, "Incorrect username or password", None)


# registers a new user by adding their info to the db
# returns the unique user_id so that it can be added to the session in app.py
def registerUser(username: str, password: str):
    insertUser(username, password)


# creates a blog by inserting the necessary data into the db
def createBlog(user_id: int, username: str, blog_title: str, date_created: str, blog_bio: str):
    insertBlog(user_id, username, blog_title, date_created, blog_bio)


# closes the database (only use if user logging out i think)
def close():
    db.close()


# Helper functions (DO NOT USE IN app.py):


# inserts a new user into the users table
def insertUser(username: str, password: str):
    command = 'INSERT INTO users VALUES ("{}", "{}", NULL);'.format(
        username, password)

    c.execute(command)
    db.commit()


# inserts a new blog into the blogs table
def insertBlog(user_id: int, username: str, blog_title: str, date_created: str, blog_bio: str):
    command = 'INSERT INTO blogs VALUES ({}, "{}", "{}", NULL, "{}", "{}");'.format(
        user_id, username, blog_title, date_created, blog_bio)

    c.execute(command)
    db.commit()


# inserts a new entry into the entries table
def insertEntry(blog_id: int, username: str, entry_title: str, entry_content: str, date_created: str):
    command = 'INSERT INTO entries VALUES ({}, "{}", NULL, "{}", "{}", "{}");'.format(
        blog_id, username, entry_title, entry_content, date_created)

    c.execute(command)
    db.commit()


# For testing only
if __name__ == "__main__":
    createTables()
    registerUser("blah", "blahblah")
    registerUser("ben", "dover")
    print(getUserId("ben"))
    createBlog(getUserId("ben"), "ben", "Doodoo",
               "10/12/2020", "This is my blog.")

    command = 'SELECT * FROM blogs'
    for row in c.execute(command):
        print(row)

    print(checkLogin("benn", "dover"))