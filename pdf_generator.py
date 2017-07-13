#To generate 2 pdfs: 1.Title page and 2.Reference page

from reportlab.pdfgen import canvas
import csv
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4,letter
from PyPDF2 import PdfFileWriter, PdfFileReader
import StringIO
from pyPdf import PdfFileReader, PdfFileWriter
import os
from reportlab.lib.pagesizes import letter,A4
import sys
from pymongo import MongoClient
from pprint import pprint

temp = sys.argv[1]
client =MongoClient()
db = client['noteshare-dev']
data = [d for d in db.files.find() if temp in d['fileLocation']][0]

directory = "web/files/temp/"
size = len(directory)
user = db.users.find_one({'_id':data['uploadedBy']})

uid = user['uid']

packet = StringIO.StringIO()
packet1 = StringIO.StringIO()

pdf = PdfFileReader(file(sys.argv[1], 'rb'))
# function to generate the title (first) page
def title_page():
	temp = sys.argv[1]
	data = [d for d in db.files.find() if temp in d['fileLocation']][0]
	if not data:
		print "no data"
	fileName = data['filename']
	clg=data['college']
	dept=data['department']
	course=data['details']['courseName']
	db.files.update({'_id':data['_id']},{'$set':{'modified':True}})
	c = canvas.Canvas(packet, pagesize=A4)
	for i in range (pdf.getNumPages()):
		#text = "Page %s" % c.getPageNumber()
		c.setFont("Helvetica-Bold",22)
		c.setStrokeColorRGB(0,0.5,0.5)
		c.setFillColorRGB(0.2,0.3,0.5)
		c.drawCentredString(300,478, str(fileName))
		c.setFont("Helvetica-Bold",18)
		c.setFillColorRGB(0,0,0)
		c.setFont("Helvetica-Bold",18)

		c.drawCentredString(300, 420, str(dept))
		c.rect(10,10, 575, 822)
		c.setFont("Helvetica",18)
		c.drawCentredString(300, 390, str(clg) )
		c.line(96, 457, 500, 457)
		c.showPage()
	c.save()
	output = PdfFileWriter()

	existing_pdf = PdfFileReader(file("Template.pdf", "rb"))
	new_pdf = PdfFileReader(packet)
		
	#move to the beginning of the StringIO buffer in every iteration to add a new page

	for i in range(1):	
		
		packet.seek(0)
		page = existing_pdf.getPage(i)
		page.mergePage(new_pdf.getPage(i))
		output.addPage(page)

	# finally, write "output" to a real file
	print "Title"
	outputStream = file("Title.pdf", "wb")
	output.write(outputStream)
	# close the file
	outputStream.close()

#function to generate reference (last) page

def reference_page_gen():
	output = PdfFileWriter()
	c1 = canvas.Canvas(packet1, pagesize=A4)
	for i in range (pdf.getNumPages()):
		c1.setFont("Helvetica-Bold", 24, leading = None) 
		c1.setStrokeColorRGB(0,0.5,0.5)
		c1.setFillColorRGB(0.2,0.3,0.5)

		c1.drawString(50,700, "References:")
		c1.setFont("Helvetica", 12, leading = None)
		c1.drawString(50, 650-14, "http://www.noteshare.in/profile/"  + uid)
		c1.setStrokeColorRGB(0,0,0)
		c1.rect(10,10, 575, 822)

	c1.showPage()
	c1.save()

	existing_pdf = PdfFileReader(file("Template.pdf", "rb"))
	new_pdf = PdfFileReader(packet1)
	
	for i in range(1):	
			
		packet.seek(0)
		#to add the NoteShare url and page no. (which is the new pdf) on the existing page
		page = existing_pdf.getPage(i)
		page.mergePage(new_pdf.getPage(i))
		output.addPage(page)

	
	
	outputStream = file("Reference.pdf", "wb")
	output.write(outputStream)
	# close the file
	print "Reference"

	outputStream.close()


def pdf_shrink():
	
	output = PdfFileWriter()
	
	for i in range (pdf.getNumPages()):
		p = pdf.getPage(i)
		
		for box in (p.mediaBox, p.cropBox):	

		    box.lowerLeft = (box.getLowerLeft_x() - 20, box.getLowerLeft_y() - 20)		                     
		    box.upperRight = (box.getUpperRight_x() + 20,  box.getUpperRight_y() + 10)

		output.addPage(p)
	

	#finally write the "output" to a real file
	print "Revised"
	
	outputStream = file("Revised.pdf", "wb")
	output.write(outputStream)
	outputStream.close()


if __name__ == '__main__':
	title_page()
	reference_page_gen()
	pdf_shrink()