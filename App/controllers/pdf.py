import fitz
import os
import requests
from Crypto.Cipher import AES
# from .open_ai import prompt
from pyre_base import uploadPDF

key = b'/xeej/xb8/x0c/x97/xe9j/xba,W/xcb'
IV = os.urandom(16)

filename = "A_Deep_Learning_Approach_for_Efficient_Palm_Reading.pdf"
file = open(filename, 'rb')

def create_doc_image(file_name):
    try:
        new_file = file_name.split(".")[0]
        doc = fitz.open(file_name)
        first_page = doc[0]
        image = first_page.get_pixmap()
        image.save(f"images/{new_file}.png")
        #can upload file here one time or do it in a separate function
        #if added swap return value to be the url returned from upload function
        return True
    except:
        return False #change to None if file upload is included

def get_information(file_name):
    
    stop_words = ["keywords","abstract"]
    stop_word_loc = {"keywords": "","abstract": ""}
    contents = {}
    # file = f"documents/{file_name}"
    file_open = fitz.open(file_name)
    for word in stop_words:

        for page in file_open:
            locations = page.search_for(word)

            if len(locations) != 0:
                if stop_word_loc[word] == '':
                    stop_word_loc[word] = page.number

    if stop_word_loc["abstract"] is not None:
        contents["abstract"] = file_open[stop_word_loc["abstract"]].get_text()
        request = f"Extract the entire Abstract section from the following text'{contents['abstract']}'"
        abstract  = prompt(request)["choices"][0]["text"]
        abstract = abstract.replace(abstract[:10], '')
        
    if stop_word_loc["keywords"] is not None:
        contents["keywords"] = file_open[stop_word_loc["keywords"]].get_text()
        request = f"Extract the Keywords section from the following as a python list'{contents['keywords']}'"
        key_list  = prompt(request)["choices"][0]["text"]
        key_list = key_list.split('[')[1].strip(']').split(',')
        
        keywords = []
        for key in key_list:
            keywords.append(key.strip(' ').strip('"').strip("'"))

    # request = f"Extract the authors from the following text '{file_open}'"
    # authors  = prompt(request)["choices"][0]["text"]
    # print(authors)

    return keywords, abstract

def encrypt_pdf(file, id):
    data = file.read()
    cipher = AES.new(key=key, mode=AES.MODE_CBC, IV=IV)
    for n in range(0, 16-len(data)%16):
        data = data + bytes(" ", encoding="utf-8")
    encryptedFile = cipher.encrypt(data)
    f = open(f"App/uploads/{id}.pdf", "wb")
    f.write(encryptedFile)
    f.close()
    os.remove(f"App/uploads/{id}.pdf")
    url = uploadPDF(id, f"{id}.pdf")
    print(url)

url = ""    
def decrypt_pdf_from_url(url):
    response = requests.get(url)
    data = response.text
    data = data[:(len(data)-len(data)%16)-1]
    # data = data[:int(len(data)/16)*16]
    cipher = AES.new(key, AES.MODE_CBC, IV=IV)
    for n in range(1, 17):
        print(n)
        print(bytes(str(n), encoding="utf-8"))
        data = data + str(bytes(str(n), encoding="utf-8"))
        try:
            decryptedFile = cipher.decrypt(data)
            f = open("App/uploads/1.pdf", "wb")
            f.write(decryptedFile)
            f.close()
        except ValueError as v:
            print(v)
        
# encrypt_pdf(file, 1)
# decrypt_pdf_from_url(url)

message = "12345678901234567"
with open("test.pdf", "w") as f:
    cipher = AES.new(key=key, mode=AES.MODE_CBC, IV=IV)
    i=0
    while (len(message)%16 != 0):
        message += ' '
        i += 1
        print(i)
    crypt = cipher.encrypt(message)
    f.write(crypt.decode("CBC-AES128"))
    f.close()