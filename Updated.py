import random
import time
import getpass
import os
import smtplib
import webbrowser
import bcrypt
import mysql.connector
#SQL DB
db = mysql.connector.connect(
    host = os.environ.get('SQL_w'),
    user = os.environ.get('SQL_u'),
    passwd = os.environ.get('SQL_p'),
    database = 'passwordmanager')

hashvar = bytes(os.environ.get('word.dll'), 'utf-8')
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(hashvar, salt).decode()
#gets rid of b'
characters = 'abcdefghijkmnopqrstuvwyzABCDEFGHJKLMNPQRSTUVWYZ123456790@#$%&'
email = os.environ.get('email')
#to enable OTP, must allow less secure apps https://myaccount.google.com/lesssecureapps

def show_accounts () :
    print ("Presented in the format 'Website', 'Username'")
    mycursor = db.cursor()
    mycursor.execute('SELECT website, username FROM Accounts')
    for x in mycursor:
        print (x)
    menu () 

def delete_account () :
    print ("Presented in the format 'Website', 'Username'")
    mycursor = db.cursor()
    mycursor.execute('SELECT website, username FROM Accounts')
    for x in mycursor:
        print (x)
    website1 = input ('What is the name of the website of the account you wish to delete? ')
    username1 = input ('What is the username of the account you wish to delete? ')
    mycursor.execute('DELETE from Accounts where username = %s and website = %s', (username1, website1))
    db.commit()
    menu ()

def authenticate () :
# Confirm authentication by sending OTP
    #create smtp session, #587 is a port number  
    smtp = smtplib.SMTP('smtp.gmail.com', 587) 
    # start TLS for E-mail security 
    smtp.starttls()
    # Log in to your gmail account
    smtp.login(email, "insertpassword")
    # remember to input the password ' ')
    otp = random.randint(1000, 9999) #4 digit
    otp = str(otp)
        
    smtp.sendmail(email, email, otp)
    # sender, recipient, content of email 
    print('OPT has successfully been sent to', email)
    smtp.quit()

    code = input ('Please type in the code: ')
    if code == otp:
        print ('Code has been verified')
        retrieve_password ()
    else:
        print ('Invalid Code')
        menu ()

def retrieve_password () :
    website = input ('For which account would you like the password for? Please input the name of the website/application: ')
    mycursor = db.cursor()
    mycursor.execute (('SELECT password FROM Accounts WHERE website = %s'), (website,))
    for x in mycursor:
        print (x)
        menu()
    else:
        print ('Account does not exist')
        menu()

def update_account() : 
    print ("Presented in the format 'Website', 'Username'")
    mycursor = db.cursor()
    mycursor.execute('SELECT website, username FROM Accounts')
    for x in mycursor:
        print (x)
    options = input ('Would you like to update your username or password? ')
    if options == 'username' or options == 'Username':
        username1 = input ('What is your old username? ')
        username2 = input ('What is your new username? ')
        mycursor.execute('Update Accounts SET username = %s WHERE username = %s', (username2, username1))
        db.commit()
    #need to figure a way to add in if the command was successful or not 
    if options == 'password' or options == 'Password':
        website1 = input ('What is your account for? ')
        password2 = input ('What is your new password? ')
        mycursor.execute('Update Accounts SET password = %s WHERE website = %s', (password2, website1))
        db.commit()
    else: 
        print ('Invalid Input')
        exit()

def generatepassword () :
    length = int(input('How long would you like your password to be? (Minimum 12 characters): '))
    password = ''
    if length >= 12 :
        for x in range (0, length) :
            passchar = random.choice(characters)
            password = password + passchar
        print ('Unique Password:', password)
        proceed = input ('Would you like to save the generated password? Yes/No? ')
        if proceed == 'yes' or proceed == 'Yes' :
            time.sleep(1)
            print ('Saving and encrypting password......')
            website = str(input('Website/Application: '))
            username = str(input('Your username: '))   
            mycursor = db.cursor()
            mycursor.execute('INSERT INTO Accounts (website, username, password) VALUES (%s,%s,%s)', (website, username, password))
            db.commit()
            print ('Done! Your details have been saved')    
            menu()
        elif proceed == 'no' or proceed == 'No' :
            menu()
    else:
        print('Invalid input! \nPassword must be atleast 12 characters long!')

def menu () :
    choice = (input ('\nWelcome to your very own Password Manager! Please select from one of the options below: \n 1. Generate and Store Password \n 2. Search for Password \n 3. Delete Account Data \n 4. Show list of all Accounts \n 5. Update Password/Username \n 6. Has my password been pwned? \n 7. Exit \n' ))
    if choice == '1' :
       generatepassword ()
    elif choice == '2' :
        #authenticate () #if less seucre app access enabled
        retrieve_password () #if less secure app access disabled 
    elif choice == '3' :
        delete_account ()
    elif choice == '4' :
        show_accounts ()
    elif choice == '5' :
        update_account()
    elif choice == '6' :
        webbrowser.open('https://haveibeenpwned.com/Passwords')
        menu ()
    elif choice == '7' :
        exit ()    
    else:
        print ('Invalid input. Please input a number between 1-5')
        menu()
      
#Using the getpass module, hides the input of the password 
def masterkey () :
    input = getpass.getpass(prompt = 'Please provide the master password to start using the Password Manager: ')
    passbyte = bytes (input, 'utf-8')
    pwd = bcrypt.hashpw(passbyte, salt).decode()
    if pwd == hashed :
        print ('Login Successful!')
        menu ()
    else: 
        print ('Login Unsuccessful! \nBye!')
        exit ()


masterkey ()
