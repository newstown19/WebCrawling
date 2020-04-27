import os 
import sqlite3
from bs4 import BeautifulSoup
import requests
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-celeb", "--name", required=True,nargs='+',
   help="name of the Celebrity")
args = vars(ap.parse_args())

def URL(entity_name):
    entity_name = entity_name.lower()
    first , sir = entity_name.split(" ")
    url = "https://www.celebrities-galore.com/celebrities/" + first + "-" + sir + "/personality-number"
    return url

celeb = " ".join(args['name'])
try:
    
    req = requests.get(URL(celeb)).text
    soup = BeautifulSoup(req , 'lxml')
    div_img = soup.find('div' ,class_ ='photo-container')
    img_src = div_img.find('img')['src']
    print(img_src)
    clss = soup.find('div' , class_= 'page_content_padding')
    with open('input.txt' , 'w') as f:
        for para in clss.find_all('p'):
            f.write(para.text)
            f.write('\n')
    f.close()    
    with open('img.jpg' , 'wb') as file:
        res = requests.get(img_src)
        file.write(res.content)
    file.close()    
except Exception as e:
        print(e)

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

try:
    with open('input.txt' , 'r') as f:
        txt = f.read()
    f.close()    
    sqliteConnection = sqlite3.connect('celebrities.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")
    sqlite_insert_blob_query = """ INSERT INTO celebs
                              (Name, image , personality) VALUES (?, ?, ?)"""
    empPhoto = convertToBinaryData('img.jpg')
    
        # Convert data into tuple format
    data_tuple = (celeb,empPhoto,txt)
    cursor.execute(sqlite_insert_blob_query, data_tuple)
    sqliteConnection.commit()
    print("Image and file inserted successfully as a BLOB into a table")
    cursor.close()

except sqlite3.Error as error:
    print("Failed to insert blob data into sqlite table", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("the sqlite connection is closed")
        os.remove('input.txt')
        os.remove('img.jpg')

        
    
    
