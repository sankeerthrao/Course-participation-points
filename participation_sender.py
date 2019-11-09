#!/usr/bin/env python3

import csv
import getpass
import requests
import smtplib
import ssl
from email.mime.text import MIMEText

TEST = True

def format_message(email_row):
    if int(email_row['points']) != 1:
        email_row['plural'] = "s"
    else:
        email_row['plural'] = ""
    if email_row['no_clicker'] == "1":
        email_row['no_clicker_text'] = "<p>Our records show that you have not registered an iClicker. If you are using an iClicker, please fill out this form with your clicker ID so that we can give you credit for any lectures you have attended: <a href=\"https://docs.google.com/forms/d/12m6cSDuiEizaNAbCK2Dgn0OpUIMLgoucnTmS7pbV1qc\">https://docs.google.com/forms/d/12m6cSDuiEizaNAbCK2Dgn0OpUIMLgoucnTmS7pbV1qc</a></p>"
    else:
        email_row['no_clicker_text'] = ""
    message = """<p>Hi {first_name},</p>

<p>As of November 5, you have earned {points} participation point{plural} in CSE 105. This point does not yet include the November 6 lecture or the November 6-8 discussion sections.</p>

{no_clicker_text}

<p>It takes 20 points to earn full marks in the participation component of your grade (10%). With fewer than 20 points, we will prorate the 10%.</p>

<p>In the weeks ahead, you can still earn 6 more participation points from iClicker questions in lecture, 5 more points from attending discussion sections, and up to 10 more points from review quizzes.</p>

<p>If you are no longer enrolled in CSE 105, please reply to this email so that we may exclude you from future points annoucements.</p>

<p>-- CSE 105 Instructional Staff</p>

""".format(**email_row)
    return message

def read_roster(filename):
    roster = {}
    with open(filename) as roster_file:
        roster_reader = csv.DictReader(roster_file)
        for row in roster_reader:
            pid = row['PID'].upper()
            roster[pid] = {'first_name': row['Name'].split(" ")[0],
                           'name': row['Name'],
                           'PID': pid,
                           'email': row['Email']}
    return roster

def read_points(filename):
    points = []
    with open(filename) as points_file:
        points_reader = csv.DictReader(points_file)
        for row in points_reader:
            points.append({'first_name': row['First Name'],
                           'PID': row['Student ID'].upper(),
                           'points': row['Total Participation Points'],
                           'no_clicker': row['no_clicker']})
    return points

if __name__ == '__main__':
    email_password = getpass.getpass("Enter your university email password (not JSOE):")
    log = open('send_log.txt','w')
    
    if TEST == True:
        roster_fn = 'roster_test.csv'
        points_fn = 'points_test.csv'
    else:
        roster_fn = 'CSE_105_Fall_2019_roster_REMOVEWHENREADY.csv'
        points_fn = 'participation_points_REMOVEWHENREADY.csv' 

    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    server = smtplib.SMTP('smtp.ucsd.edu', 587)
    #Next, log in to the server
    server.ehlo()
    server.starttls(context=context)
    server.login('mborkows@ucsd.edu', email_password)

    roster = read_roster(roster_fn)
    points = read_points(points_fn)
    print("Running the main Loop")
    count = 0
    for student in points:
        if student['PID'] in roster.keys():
            roster_entry = roster[student['PID']]
            email_row = {'first_name': student['first_name'],
                         'email': roster_entry['email'],
                         'points': student['points'],
                         'no_clicker': student['no_clicker']}
            email_text = format_message(email_row)

            email_msg = MIMEText(email_text, 'html')
            email_msg['Subject'] = "CSE 105 Participation Points"
            email_msg['From'] = "Michael Borkowski <mborkows@ucsd.edu>"
            email_msg['To'] = email_row['email']

            #Send the mail
            server.sendmail('Michael Borkowski <mborkows@ucsd.edu>',email_row['email'], email_msg.as_string())
            log.write(email_msg.as_string() + "\n")
            count += 1
        else:
            print("Failed to match on {PID} ({first_name})".format(**student))
    server.close()
    log.close()
    print("Total send count: {0}".format(count))
