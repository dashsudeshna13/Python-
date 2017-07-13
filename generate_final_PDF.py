#To add margin, page no., and NoteShare url to the final document and save it   

from pyPdf import PdfFileReader, PdfFileWriter
import os
from random import randint
import sys

import StringIO
from reportlab.pdfgen import canvas
import csv
from reportlab.lib.pagesizes import letter,A4

from pymongo import MongoClient

client =MongoClient()
db = client['noteshare-dev']

directory = "web/files/temp/"
size = len(directory)

packet = StringIO.StringIO()

# create a new PDF with Reportlab 
#open the database to read fileName from it
temp = sys.argv[1]

data = [d for d in db.files.find() if temp in d['fileLocation']][0]
user = db.users.find_one({'_id':data['uploadedBy']})

uid = user['uid']
if not data:
	print "no data"	

fileName = data['filename']
c = canvas.Canvas(packet)
existing_pdf = PdfFileReader(file("merged.pdf", "rb"))

for i in range (existing_pdf.getNumPages()):
	p = existing_pdf.getPage(1).mediaBox

	text = "Page %s" % c.getPageNumber()
	c.setFillColorRGB(0,0,0)
	c.setFont("Times-Italic", 12)
	if i > 0 and i < existing_pdf.getNumPages()-1:
		c.drawString(p.getLowerLeft_x() + 20 , p.getUpperLeft_y() - 15 , "http://www.noteshare.in/profile/"  + uid)
		c.drawCentredString(p.getLowerRight_x()/2 - 10, p.getLowerLeft_y() + 10, text)

	c.showPage()
c.save()

finalpdf = PdfFileWriter()

existing_pdf = PdfFileReader(file("merged.pdf", "rb"))
new_pdf = PdfFileReader(packet)
	
#move to the beginning of the StringIO buffer in every iteration to add a new page

for i in range(existing_pdf.getNumPages()):	

	packet.seek(0)
	#to add the NoteShare url and page no. (which is the new pdf) on the existing page
	page = existing_pdf.getPage(i)
	page.mergePage(new_pdf.getPage(i))
	finalpdf.addPage(page)

# finally, write "output" to a real file
print "generating final pdf"

outputStream = file(sys.argv[1], "wb")
finalpdf.write(outputStream)
# close the file
outputStream.close()