# pip install mysql-connector-python
# pip install bcrypt
import bcrypt
import mysql.connector

f = open("pwd.txt", "r")
pwd = (f.read())
# "pwd.txt" will not be included in GitHub for security reasons.
mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password=pwd,
                               database='messaging_333')

mycursor = mydb.cursor()
# connected
signed_in = False
# Shows if the user is already signed in


def login():
    global signed_in
    while True:

        username = input("""
What is user name?
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
    else:
        print("It doesn't match")
        signed_in = False
# login()
def send_message():
    username = input("""
What is your username?""")
    # remove later; have credentials already completed and remembered if the user previously logged in.
    mycursor.execute(f"""Select * from accounts WHERE username = "{username}" """)
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
    old_max_id = mycursor.fetchone()
    # myresult = str(myresult)
    old_max_id = old_max_id[0]
    new_max_id = old_max_id + 1

    mycursor.execute(f"""
    INSERT INTO message (message_id, account_id, message, username)
    VALUES ("{new_max_id}", "{sql_account_account_id}", "{pending_message}", "{username}");""")

    mydb.commit()
send_message()