
from pdf2image import convert_from_path
import pytesseract
import io
import os
from PyPDF2 import PdfReader,PdfWriter






pdf_file_path = 'Sejarah Tingkatan 1.pdf'
file_base_name = 'sejarah_index'

pdf = PdfReader(pdf_file_path)


pages = [5,6] # page 6,7
pdfWriter = PdfWriter()

for page_num in pages:
    pdfWriter.add_page(pdf.pages[page_num])

with open('{0}_subset.pdf'.format(file_base_name), 'wb') as f:
    pdfWriter.write(f)
    f.close()

# convert page 7,8 to image and use tessearct ocr to extract

pages = convert_from_path('sejarah_index_subset.pdf',poppler_path = r"C:\Users\user\Documents\poppler-0.68.0\bin")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'



pdf_path = 'sejarah_index_subset.pdf'
output_filename = "topics_index.txt"
pg_cntr = 1


sub_dir = str("images/" + pdf_path.split('/')[-1].replace('.pdf','')[0:20] + "/")
if not os.path.exists(sub_dir):
    os.makedirs(sub_dir)

for page in pages:

    filename = "pg_"+str(pg_cntr)+'_'+pdf_path.split('/')[-1].replace('.pdf','.jpg')
    page.save(sub_dir+filename)
    with io.open(output_filename, 'a+', encoding='utf8') as f:
        f.write(str(pytesseract.image_to_string(sub_dir+filename)))
    pg_cntr = pg_cntr + 1