ZZZZZZEN Personal Project

import random
import hashlib
import time
import sys
import getpass
import os
import smtplib
from cryptography.fernet import Fernet
import webbrowser

fkey = open ('file_key.txt', 'rb')
key = fkey.read()
cipher = Fernet(key)
characters = 'abcdefghijkmnopqrstuvwyzABCDEFGHJKLMNPQRSTUVWYZ123456790@#$%&'
email = 'insert email here'
#to enable OTP, must allow less secure apps https://myaccount.google.com/lesssecureapps

def show_accounts () :
    handle = open ('Password.txt', 'r')
    print ('Fetching account data:')
    for line in handle : 
        account = line.split(':')[0]
        print (account)
    menu () 

def delete_account () : 
    handle = open ('Password.txt','r')
    erase = input ('Which account would you like delete: ')
    new_data = []
    str = erase
    for line in handle :
        if not line.startswith (erase):
            new_data.append(line)
    #adds all the lines that does not start with 'str' input        
    handle.close ()
    handle = open ('Password.txt', 'w')
    handle.writelines(new_data)
    handle.close()
    time.sleep(1)
    print('Please wait while we delete your', str, 'account data')
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
    otp = random.randint(1000, 9999) #generates a 4 digit number for OTP
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
    handle = open ('Password.txt', 'r')
    account = input ('For which account would you like the password for? Please input the name of the webiste/application: ')
    for line in handle :
        if line.startswith (account) :
            pwd = line.split(':')[2]
            print (pwd)
        else:
            print('Account does not exist!')    
        menu ()
        
def generatepassword () :
    website = str(input('Website/Application: '))
    username = str(input('Your username: '))
    length = int(input('How long would you like your password to be? (Minimum 12 characters: '))
    password = ''
    if length >= 12 :
        for x in range (0, length) :
            passchar = random.choice(characters)
            password = password + passchar
    
        print ('Unique Password:', password)
        time.sleep(1)
        print ('Saving and encrypting password......')
        #encrypt whole file   
        time.sleep (2)
        print ('Done! Your details have been saved')
        
    else:
        print('Invalid input! \nPassword must be atleast 12 characters long!')

    f = open ('Password.txt', 'a')
    f.write (f'{website}:{username}:{password}\n')
    f.close()
    menu()

def encrypt (filename, key) :
    #Given a filename (str) and key (bytes), encrypt file and write it 
    with open('Password.txt', 'rb') as file:
        f = file.read()
        encrypted_f = cipher.encrypt(f)
    with open ('Password.txt', 'wb') as file: 
        file.write(encrypted_f)

def decrypt (filename, key) :
    with open('Password.txt', 'rb') as file:
        encrypted_f = file.read()
        decrypted_f = cipher.decrypt(encrypted_f)
    with open ('Password.txt', 'wb') as file:
        file.write (decrypted_f)

def menu () :
    choice = (input ('\nWelcome to your very own Password Manager! Please select from one of the options below: \n 1. Generate and Store Password \n 2. Search for Password \n 3. Delete Account Data \n 4. Show list of all Accounts \n 5. Encrypt/Decrypt \n 6. Has my password been pwned? \n 7. Exit \n' ))
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
        num = input ("Would you like to decrypt or encrypt current file: Please select '1' to encrypt or '2' to decrypt file: ")
        if num == '1':
            encrypt ('Password.txt', key)
            print ('File encryption complete')
            menu ()
        elif num =='2':  
            decrypt ('Password.txt', key)  
            print ('File decryption complete') 
            menu ()
        else :
            print ('Invalid output. Input must be either 1 or 2!')  
            menu ()
    elif choice == '6' :
        webbrowser.open('https://haveibeenpwned.com/Passwords')
        menu ()
    elif choice == '7' :
        encrypt ('Password.txt', key) 
        exit ()    
    else:
        print ('Invalid input. Please input a number between 1-5')
        menu()
      
#Using the getpass module, hides the input of the password 
def masterkey () :
    pwd = getpass.getpass(prompt = 'Please provide the master password to start using the Password Manager: ')
    hpass = open ('masterkey.txt', 'r')
    password = hpass.read()
    if pwd == password :
        menu ()
    else: 
        print ('Please do not hack me \nBye!')
        exit ()

decrypt ('Password.txt', key)  
masterkey ()
