from django.shortcuts import render
import mysql.connector
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import os
import cv2 as cv
import numpy as np
from hackapp.forms import *
import pytesseract
from PIL import ImageGrab
import time
from O365 import Account
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\vaibh\\appdata\\local\\programs\\tesseract-ocr\\tesseract.exe"

def home(request):
    data = displaytable(request.user.username)
    return render(request, 'home.html', {'data':data})



@login_required
def mail(request):
    if request.method == 'GET':
        return render(request, 'mail.html', {'form': MailForm()})
    
    if request.method == 'POST':
        client_id = 'f38a489d-d4a0-4ae8-ad0f-0bf78d43ab34'  # Your client_id
        client_secret = '79q8Q~Lgyc3T~fcujHIp-ovB3U4OvxE7TQW85bHP'  # Your client_secret, create an (id, secret)
        tenant_id1 = 'f8cdef31-a31e-4b4a-93e4-5f571e91255a'
        print("Connecting to O365")
        account = Account(credentials=(client_id, client_secret)) 
        if account.authenticate(scopes=['basic', 'MailboxSettings.ReadWrite','Mail.ReadWrite', 'Mail.Send','offline_access']):
            print('Authenticated!')
        mailbox = account.mailbox()
        inbox = mailbox.inbox_folder()
        message = mailbox.new_message()
        message.to.add(emaillisttable(request.user.username))
        message.body = request.POST.get('Email')
        message.subject = request.POST.get('Subject')
        message.send()
        return render(request, 'home.html')
        
@login_required
def event(request):
    if request.method == 'GET':
        return render(request, 'event.html', {'form':EventForm()})
    else:
        createeventtable(request.user.username, request.POST.get('Eventname'))
        return redirect('checkin', request.POST.get('Eventname'))

    
@login_required
def checkin(request, eventname):
    if request.method == 'GET':
        tabledata = displayevent(request.user.username, eventname)
        return render(request, 'checkin.html', {'eventname':eventname, 'data':tabledata})

    if request.method == 'POST':
        #eventname = request.POST.get('Eventname')
        print(eventname)

        ################################################################################# scan in ################################################################################

        capture = cv.VideoCapture(0)
        fullname = []
        start_time = time.time()
        while True:
            if (time.time() - start_time > 4):
                break

            isTrue, frame = capture.read()
            data = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)
            
            for i, word in enumerate(data['text']):
                if int(data['conf'][i]) > 90:  # Filter out low confidence words
                    if (len(word) > 2 and 
                        (not all(char.isspace() for char in word)) and 
                        (word[0] not in '0123456789') and 
                        (word[1] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') and
                        (word not in fullname)):
                        print("Word:" + word +":" + str(data['conf'][i]))
                        fullname.append(word);
            
        capture.release()
        print("array:", fullname)
        print('DONE')

        ################################################################################  ################################################################################

        edge_options = webdriver.ChromeOptions()
        edge_options.add_argument('--headless')
        driver = webdriver.Chrome(options=edge_options)
        driver.get("https://www.purdue.edu/directory/")
        search_bar = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'basicSearchInput'))
        )

        if (len(fullname) == 0):
            tabledata = displayevent(request.user.username, eventname)
            return render(request, 'checkin.html', {'eventname':eventname, 'data':tabledata})
            
        keyworddir = fullname[0] + " " + fullname[1]
        print("keyword",keyworddir)
        search_bar.send_keys(keyworddir)
        search_bar.submit()
        driver.implicitly_wait(5)
        error_check = driver.find_element(By.ID, "results")
        if error_check.text == "Sorry, nothing matches your query.":
            print("does not exists")
        else:
            search_results = driver.find_element(By.CLASS_NAME, "more")
            a = search_results.text
            stringa = a.split("EMAIL ")[1]
            stringb = stringa.split("\n")[0]
            print("email is: ", stringb)
            checkintable(request.user.username, stringb, eventname)
            driver.quit()
        tabledata = displayevent(request.user.username, eventname)
        return render(request, 'checkin.html', {'eventname':eventname, 'data':tabledata})
    

def signupuser(request):

    if request.method == 'GET': 
        return render(request, 'signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
                
            except IntegrityError:
                return render(request, 'signupuser.html', {'form':UserCreationForm(), 'error':'Username taken'})
                
        else:
            return render(request, 'signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET': 
        return render(request, 'loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('home')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    


def emaillisttable(organizer):
    try: 
        con = mysql.connector.connect(host='localhost', user='root', passwd='mysql_root123', db='hackathon')
        if con.is_connected():
            print('email list table Connection established')
            cursor = con.cursor()
            query1 = "SELECT Email FROM {}"
            cursor.execute(query1.format(organizer))
            emailist = cursor.fetchall()
            returner = []
            for email in emailist:
                 returner.append(email[0])
            return returner
            
        else:
            print('connection to database not established')
            return []
    except mysql.connector.Error as e:
            print(e)
            return []

def createeventtable(organizer, eventname):
    try:
        con = mysql.connector.connect(host='localhost', user='root', passwd='mysql_root123', db='hackathon')
        if con.is_connected():
            print('create event table Connection established')
            cursor = con.cursor()
            query1 = "CREATE TABLE IF NOT EXISTS {} (Email VARCHAR(50) PRIMARY KEY)"
            cursor.execute(query1.format(organizer))
            query2 = "ALTER TABLE {} ADD COLUMN {} INT"
            cursor.execute(query2.format(organizer, eventname))
            con.commit()
            con.close()
        else:
            print('connection to database not established')
          
    except mysql.connector.Error as e:
            print(e)

def checkintable(organizer, useremail, eventname):
    try:
        con = mysql.connector.connect(host='localhost', user='root', passwd='mysql_root123', db='hackathon')
        if con.is_connected():
            print('chec in table Connection established')
            cursor = con.cursor()
            query1 = "INSERT INTO {} (Email, {}) VALUES ('{}', 1) ON DUPLICATE KEY UPDATE {} = 1;"
            cursor.execute(query1.format(organizer, eventname, useremail, eventname))
            con.commit()
            con.close()
        else:
            print('connection to database not established')
            
    except mysql.connector.Error as e:
            print(e)

def displaytable(organizer):
    try:
        con = mysql.connector.connect(host='localhost', user='root', passwd='mysql_root123', db='hackathon')
        if con.is_connected():
            cursor = con.cursor(dictionary=True)
            query="CREATE TABLE IF NOT EXISTS {} (Email VARCHAR(50) PRIMARY KEY)"
            cursor.execute(query.format(organizer))
            con.commit()
            query1 = "select * from {};".format(organizer)
            cursor.execute(query1.format(organizer))
            return cursor.fetchall()
        else:
            print('connection to database not established')
            return []
            
    except mysql.connector.Error as e:
            print(e)
            return []
    
def displayevent(organizer, eventname):
    try:
        con = mysql.connector.connect(host='localhost', user='root', passwd='mysql_root123', db='hackathon')
        if con.is_connected():
            cursor = con.cursor(dictionary=True)
            query="CREATE TABLE IF NOT EXISTS {} (Email VARCHAR(50) PRIMARY KEY)"
            cursor.execute(query.format(organizer))
            con.commit()
            query1 = "select Email, {} from {};".format(eventname, organizer)
            cursor.execute(query1.format(organizer))
            return cursor.fetchall()
        else:
            print('connection to database not established')
            return []
            
    except mysql.connector.Error as e:
            print(e)
            return []
