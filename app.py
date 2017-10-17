# Flabbergasted: Eugene Thomas and Joyce Wu
# SoftDev1 pd7
# HW10 -- Average, ... or maybe just Basic
# 2017-10-18

#IMPORTING
#=====================================================================================
import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
## from flask import Flask, request, render_template, session, redirect, url_for, flash
## import os
#=====================================================================================

## app = Flask(__name__) #create instance of class
## app.secret_key = os.urandom(32)

ACCOUNTS = {}
INFORMATION = {}

# OPEN FILES:
#=====================================================================================
file1 = open('peeps.csv')
d1 = csv.DictReader(file1)
file2 = open('courses.csv')
d2 = csv.DictReader(file2)
f="discobandit.db"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops
#=====================================================================================

#INSERT YOUR POPULATE CODE IN THIS ZONE / POPULATE INFORMATION
#=====================================================================================
command = "CREATE TABLE STUDENT(NAME TEXT, AGE INTEGER, ID INTEGER)"
c.execute(command)    #run SQL statement
command = "CREATE TABLE COURSES(CODE TEXT, MARK INTEGER, ID INTEGER)"
c.execute(command)    #run SQL statement
for row in d1:
    name = row['name']
    age = row['age']
    Id = row['id']
    command = "INSERT INTO STUDENT VALUES('" + name + "', " + age + ", " + Id + ")"
    c.execute(command) #run SQL statement
for row in d2:
    code = row['code']
    mark = row['mark']
    Id = row['id']
    command = "INSERT INTO COURSES VALUES('" + code + "', " + mark + ", " + Id + ")"
    c.execute(command) #run SQL statement
#=====================================================================================


# FILLING UP ACCOUNTS
#=====================================================================================
command = "SELECT NAME, STUDENT.ID FROM STUDENT, COURSES WHERE STUDENT.ID = COURSES.ID;"
foo = c.execute(command)
for bar in foo:
    ACCOUNTS[bar[0]] = bar[1]
#=====================================================================================


# LOOKING UP GRADES
#=====================================================================================
def getGrades(name):
    d = {}
    ID2 = ACCOUNTS[name]
    ID  = str(ID2)
    command = "SELECT CODE, MARK FROM COURSES WHERE COURSES.ID = " + ID + ";"
    foo = c.execute(command);
    for bar in foo:
        d[bar[0]] = bar[1]
    return d
#=====================================================================================
print getGrades('kruder')

# AVERAGE METHOD
#=====================================================================================
def avg(name):
    summ = 0
    ctr = 0
    d = getGrades(name)
    for key in d:
        summ += d[key]
        ctr += 1
    return (1.0*summ) / ctr
#=====================================================================================
print avg('kruder')


# NAME, ID, AND AVERAGE:

def name_id_avg():
    rstr = "\n"
    for i in ACCOUNTS:
        rstr += i
        rstr += ", "
        rstr += str(ACCOUNTS[i])
        rstr += ", "
        rstr += str(avg(i))
        rstr += "\n"
    return rstr

print name_id_avg()

'''
### The Root Route:

@app.route('/')
def hello():
    if 'user' in session.keys(): # If there is a session...
        return render_template('grades.html', name = session['user'], ID = session['id'], avg = (avg(name)) ) # Direct to the logged in page
    else: # IF NOT...
        return render_template('login.html') # Log in

def aut(u, p):
    if (u in ACCOUNTS):
        if p == ACCOUNTS[u]:
            return 0 #All correct
        else:
            return 1 #Wrong Password
    else:
        return -1 #Wrong Username

@app.route('/login', methods=["GET", "POST"])
def login():
    if 'user' not in session:
        if aut(request.form['user'], request.form['id']) == 0:
            session['user'] = request.form['user'] # Add user to the session.
            session['id'] = request.form['id']
            print session.keys()
            return render_template('grades.html', name = session['user'], ID = session['id'], avg = (avg(name)) ) # Direct to the logged in page
        elif aut(request.form['user'], request.form['id']) == 1:
            flash('Wrong USERID')
            return render_template('login.html')
        else:
            flash('Wrong Username')
            return render_template('login.html')
    else:
        return render_template('grades.html', name = session['user'], ID = session['id'], dict = INFORMATION, avg = (avg(name)) ) # Direct to the logged in page

### After logging out:

@app.route('/logout')
def logout():
    if 'user' in session.keys():
        session.pop('user',None) ## Remove user from the session
    flash('Logged Out')
    return redirect("/")

if __name__=="__main__":
    app.debug = True
    app.run()
'''
db.commit()
db.close()  #close database
