import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)

#Next, log in to the server
#server.ehlo()
server.starttls()
server.login('sankeerth1729', 'pleaseguess')

#Send the mail
msg = "This is the test mail"
# The /n separates the message from the headers
server.sendmail('sankeerth1729@gmail.com', 'mborkowski@ucsd.edu', msg)
