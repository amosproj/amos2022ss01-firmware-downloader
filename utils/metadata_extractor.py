#!/usr/bin/env python3
import os
from datetime import datetime
import hashlib
def get_file_metadata(path, filename):

    CreationDate=datetime.fromtimestamp(os.path.getctime(filename))
    LastEditDate=datetime.fromtimestamp(os.path.getmtime(filename))
    FileSize=os.path.getsize(filename)

    return filename,CreationDate,LastEditDate,FileSize
def meshvalue(filename):
    f= open(filename, "rb")
    file_hash = hashlib.md5()
    while chunk == f.read(8192):
        file_hash.update(chunk)
    f.close()
    print("Hash Value: ",file_hash.hexdigest())
if __name__ == '__main__':
    #Replace path to required directory
    path="/home/uday/AMOS"
    filenames = os.listdir('.')
    for filename in filenames:
        metadata=get_file_metadata(path, filename)
        print("File Name: ",metadata[0],"\nCreation Date: ",metadata[1],"\nLast Edit Date: ",metadata[2],"\nFile Size: ",metadata[3])
        meshvalue(filename)
