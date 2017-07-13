from pyPdf import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
import csv
from reportlab.lib.utils import ImageReader
import os
from PyPDF2 import PdfFileWriter, PdfFileReader

def pdf_merge():
    
    """
    file name of new pdf (after merging)
    """
    output_filename = "merged.pdf"
    output = PdfFileWriter()

    """
    Get the path to the reference page(last page)
    """
    pdfOne = PdfFileReader(file( "Reference.pdf", "rb"))
    pdfTwo = PdfFileReader(file( "Title.pdf", "rb"))
    output.addPage(pdfTwo.getPage(0))

    document = PdfFileReader(file("Revised.pdf", "rb"))
    for i in range(document.getNumPages()):
        output.addPage(document.getPage(i))

    
    
    #to add the reference page to the merged document 
    output.addPage(pdfOne.getPage(0))

    # finally, write "output" to a real file, here "merged.pdf"
    with open("merged.pdf", "wb") as f:
        output.write(f)
    print "merging"    


if __name__ == '__main__':
    pdf_merge()
