# pip install mysql-connector-python
# pip install bcrypt
# pip install requests
import bcrypt
import mysql.connector
from os import path

file_pwd = open("pwd.txt", "r")
# "pwd.txt" has plain text password for the database. 
pwd = (file_pwd.read())
# "pwd.txt" will not be included in GitHub for security reasons.
file_pwd.close()
# close unneeded process to same more memory.
mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password=pwd,
                               database='messaging_333')
# connect to database with MySQL

mycursor = mydb.cursor()
# this is responsible for handling SQL commands.
signed_in = False
# Shows if the user is already signed in

actual_username = ""
# needed to transfer the username of the user across multiple functions.


def login():
    global signed_in
    global actual_username
    while True:

        username = input("""
What is username?
>""")
        if len(username) > 11:
            raise ValueError("Username is too large")
        else:
            pass
        password = input("""
What is your password?
>""")
        if len(password) > 11:
            raise ValueError("Password is too large")
        else:
            password = password.encode()
        mycursor.execute(f"""
        SELECT password FROM accounts WHERE username = "{username}" 
        """)
        # it returns all the row(s) where the username is equal to the input given by the user
        myresult = mycursor.fetchone()
        # returns the first occurring one
        # returns none if username was not able to be located
        if myresult:
            # if it located the username, it will break away from the loop
            actual_username = username
            print(actual_username)
            break
        else:
            # if it did not locate the username, it will
            print("username does not exist")
            pass
    myresult = myresult[0].encode()
    # removes the unnecessary parentheses and the single quotation mark
    if bcrypt.checkpw(password, myresult):
        # checks if the encrypted password mashes the plain text password given by the user
        print("It matches")
        signed_in = True
        # gen_pwd = open("generated_credentials.txt", "w+")
        with open("generated_credentials.txt", "w+") as text:
            text.write(f"""{username}, {password.decode()}""")
        text.close()
        print(username + "123")
    else:
        print("It doesn't match")
        signed_in = False
# login()


def send_message():
    global actual_username
    if path.exists("generated_credentials.txt"):
        with open("generated_credentials.txt", "r") as text:
            f = text.read()
        text.close()
        f = f.split(", ")
        # the file looks like this " person, password ". So, splitting it at the comma is smart.
        username = f[0]
        actual_username = username
        password = f[1]
        print(username)
    else:
        print("\nFailure to find credentials. Login in again")
        login()

    # - remove later; have credentials already completed and remembered if the user previously logged in.
    mycursor.execute(f"""Select * from accounts WHERE username = "{actual_username}" """)
    myresult = mycursor.fetchone()

    sql_account_account_id = myresult[0]
    sql_account_name = myresult[1]
    sql_account_email = myresult[2]
    sql_account_password = myresult[3]

    pending_message = input("""
What is the message you want to send?
>""")

    mycursor.execute("""
    SELECT MAX(message_id)
    FROM message
    """)
    # retrieves the row with the highest message_id number
    old_max_id = mycursor.fetchone()
    try:
        new_max_id = old_max_id[0] + 1
    except TypeError:
        new_max_id = 1
        # used for if the database has no rows/is wiped clean
    # creates the highest id number that is one larger from the second largest.

    mycursor.execute(f"""
    INSERT INTO message (message_id, account_id, message, username)
    VALUES ("{new_max_id}", "{sql_account_account_id}", "{pending_message}", "{actual_username}");""")
    # sends message into database.
    mydb.commit()


