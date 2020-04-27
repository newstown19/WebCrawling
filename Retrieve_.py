import argparse
import sqlite3
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-celeb", "--name", required=True,nargs='+',
   help="name of the Celebrity")
args = vars(ap.parse_args())

celeb = ' '.join(args['name']).lower()

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")
    file.close()
def writeTofileStr(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'w') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")
    file.close()
try:
    sqliteConnection = sqlite3.connect('celebrities.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")

    sql_fetch_blob_query = """SELECT * from celebs where Name = ?"""
    cursor.execute(sql_fetch_blob_query, (celeb,))
    record = cursor.fetchall()
    for row in record:
        print("Name = ", row[0])
        img  = row[1]
        trait = row[2]
        name = row[0]
        
        print("Storing Celebrity image and Personality traits on disk \n")
        photoPath = os.getcwd()+"\\" + name + ".jpg"
        traitPath = os.getcwd()+"\\" +name  + "_traits.txt"
        writeTofile(img, photoPath)
        writeTofileStr(trait, traitPath)
        
        cursor.close()

except sqlite3.Error as error:
    print("Failed to read blob data from sqlite table", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("sqlite connection is closed")
    
