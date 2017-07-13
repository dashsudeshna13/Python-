import smtplib
import datetime
from time import localtime
from email.mime.multipart import MIMEMultipart
import csv
from email.mime.text import MIMEText
import sched
import time
from string import Template

s = sched.scheduler(time.time, time.sleep)

# Function to schedule a mail 

def schedule_mail():

	"""
	Open the user data base for reading user name and user mail id
	Just add (change) the path of user file in open() to open it in read mode

	"""

	with open("C:\Users\D Sudeshna\Desktop\code\email_gen\User.csv", "r") as data_file:

		user_data = csv.reader(data_file, delimiter = ',')

		for row in user_data:
			user_name = row[2]
			user_mail_id = row[3]
			week = 604800
			msg = MIMEMultipart()

			# Open the recommendations file of user in read mode 

			with open("C:\Users\D Sudeshna\Desktop\code\email_gen\Recommendations.txt", "r") as rec_file:

				recs = rec_file.read()

				"""
				Variable :
				recs stores all the recommendations of user

				"""

				with open("C:\Users\D Sudeshna\Desktop\html_textNS.txt", "r+b") as html_file:

					# Open the html_text_file (for getting the template of email) in read and write mode 

					html_text = html_file.read()

					html_text = Template(html_text).safe_substitute(name = "Shubham Bobde", recs = recs);

					"""
					A substitution is made here

					user_name = stores user name taken from database
					'name' in html_file is substituted by user_name 

					recs = stores list of all recommendations taken from rec_file 
					'recs' in html_file is substituted by list of all recommedations

					"""
					

					from_addr = "d.sudeshna1998@gmail.com" # make it NoteShare mail id
					to_addr = "sbobde057@gmail.com"

					"""
					Variable:

 					from_addr : stores the sender's email address
					to_addr : stores the recipient's email address

					"""

					msg['From'] = from_addr
					msg['To'] = to_addr
					msg['Subject'] = "NoteShare Recommendations"

					msg.attach(MIMEText(html_text,'html'))
					server = smtplib.SMTP()
					server.connect("smtp.gmail.com:587")
					server.ehlo()
					server.starttls()

					# Login with NoteShare mail id and password

					server.login("d.sudeshna1998@gmail.com", "sdjaydev##")
					
					# Send the message via your own SMTP server
					
					server.sendmail(from_addr, to_addr, str(msg))

					# Stores the time at which mail is sent

					time_stamp_now = datetime.datetime.now()
				
					print "sending"
					
					# Schedule the mail; to be sent every 1 week 
					s.enter( 1*week, 1, schedule_mail, ())

					server.quit()
				
schedule_mail()
s.run()

"""
Note:

1. Dont send the same recommendations again next week
   To do that compare the present time_stamp with previous time_stamp and send the mail only if the 2 are not equal

"""