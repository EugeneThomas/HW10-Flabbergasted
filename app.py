# Flabbergasted: Eugene Thomas and Joyce Wu
# SoftDev1 pd7
# HW10 -- Average, ... or maybe just Basic
# 2017-10-18

#IMPORTING
#=====================================================================================
import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
#=====================================================================================

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
    foo = c.execute(command) #run SQL statement
    for bar in foo:
        print bar
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
#print getGrades('kruder')

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
#print avg('kruder')


# NAME, ID, AND AVERAGE:
#=====================================================================================
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
#=====================================================================================
#print name_id_avg()


# CREATING THE PEEPS_AVG TABLE
#=====================================================================================
def create_table():
    command = "CREATE TABLE peeps_avg(ID INTEGER, AVG INTEGER)"
    c.execute(command)
    for i in ACCOUNTS:
        command = "INSERT INTO peeps_avg VALUES(" + str(ACCOUNTS[i]) + ", " + str(avg(i)) + ")"
        c.execute(command)
#=====================================================================================
create_table()
command = "SELECT * FROM peeps_avg"
foo = c.execute(command)
#for bar in foo:
#    print bar

# Facilitate Changes:
#=====================================================================================
def add_row(CODE, MARK, NAME):
    command = 'INSERT INTO COURSES VALUES("' + str(CODE) + '", ' + str(MARK) + ", " + str(ACCOUNTS[NAME]) + ")"
    c.execute(command) #run SQL statement
    #print update_average(NAME)
    return NAME + " received a " + str(MARK) + " in " + CODE + "."
def update_average(NAME):
    command = "UPDATE peeps_avg SET AVG" + "= " + str(avg(NAME)) + " WHERE " + str(ACCOUNTS[NAME]) + " = ID;"
    c.execute(command)
    return NAME + "'s New Average is: " + str(avg(NAME)) + "."
#=====================================================================================

#print add_row('systems', 99, 'kruder')
#print add_row('systems', 99, 'kruder')
#print add_row('systems', 99, 'kruder')
#command = "SELECT * FROM COURSES;"
#foo = c.execute(command)
#for bar in foo:
#    print bar

print "\n\n\n\n"
cont = True
while cont == True:
    num = int(raw_input("Press 1 to add a class. Press 2 to Leave.\n"))
    if num == 1:
        sure = 0
        while sure != 1:
            course = raw_input("Please insert a course name. For sake of syntax, keep all words lowercase.\n")
            sure = int(raw_input("Are you sure about " + "'" + course + "'? Click 1 for yes. Type any other character for no.\n"))
        sure = 0
        while sure != 1:
            mark = int(raw_input("Please insert a grade. Please make it an integer.\n"))
            sure = int(raw_input("Are you sure about " + "'" + str(mark) + "'? Click 1 for yes. Type any other character for no.\n"))
        sure = 0
        while sure != 1:
            name = raw_input("For which student are you doing this? Please insert their name, with correct capitalization.\n")
            sure = int(raw_input("Are you sure about " + "'" + name + "'? Click 1 for yes. Type any other character for no.\n"))
            #print add_row(course, mark, name)
            print update_average(name)
    elif num == 2:
        cont = False;



db.commit()
db.close()  #close database
