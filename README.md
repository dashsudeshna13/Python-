Time-Based email automation system
Wrote a script in Python to send email from SMTP server.  The script takes email content and html content from .txt file. Images, videos, pdfs, can easily be sent as attachments. The script is designed to send mail after every 1 week.  The script was tested successfully by sending mail to 30 different mail ids in one go in 180 seconds.
Libraries used-
•	Email
This library is used to connect to SMTP server for sending mail. MIMEMultipart is imported from email. It is used for attaching media to the mail.

•	CSV
If we want to send a list of recommendations or new uploads to users we can do that by reading the data from a csv file and send it in the body of the mail.

•	Datetime
Every time a mail is sent, a timestamp is created and it is saved in a csv file along with a flag/status variable. The status variable shows the sent/not sent status of a mail to the user. This ensures that the same mail is not sent to the user again. Also the mail is sent only if the status is ‘not sent’ for a particular user, and it is updated to ‘sent’ after the mail is sent.


PDF generator

•	Wrote a script in Python which generates PDF with all required formatting needed in the pdf. Specifically my code generated Title and Reference page with Noteshare logo watermarked on each of the page. 
•	The notes pdf is also shrunk from sides creating space for margin, page no. and links to be inserted.
•	The first and last pages are then merged (or appended) to the notes pdf, with Title page at the front and Reference at the end.
•	The entire process takes roughly 10- 12 seconds for a pdf of size around 6 MB.
