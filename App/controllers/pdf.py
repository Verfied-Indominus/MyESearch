import PyPDF2
import re

file = "A_Deep_Learning_Approach_for_Efficient_Palm_Reading.pdf"
filecontent = ""

def pullAbstractnKeys(file_name):

    with open(f'{file}', 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        pages = len(pdf.pages)
        for x in range(pages):
            filecontent+= pdf.pages[x].extract_text()

    filecontent = re.sub(r'[^\x00-\x7F]+', '', filecontent)
    filecontent = re.sub(r'\s+', ' ', filecontent)
    first_500_words = ' '.join(filecontent.split()[:500])
    return first_500_words


