import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)

#Next, log in to the server
#server.ehlo()
server.starttls()
server.login('username', 'password')

#Send the mail
msg = "https://github.com/sankeerthrao/Course-participation-points/invitations"
# The /n separates the message from the headers
server.sendmail('sankeerth1729@gmail.com', 'mborkowski@ucsd.edu', msg)
