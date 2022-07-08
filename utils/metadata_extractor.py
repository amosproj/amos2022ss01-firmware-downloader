import os, hashlib
from datetime import datetime


def get_file_metadata(file_name):
    creation_date = datetime.fromtimestamp(os.path.getctime(file_name))
    last_edit_date = datetime.fromtimestamp(os.path.getmtime(file_name))
    file_size = os.path.getsize(file_name)
    return file_name, creation_date, last_edit_date, file_size


def mesh_value(file_name):
    with open(file_name, "rb") as file:
        file_hash = hashlib.md5()
        if file.read(8192):
            chunk = file.read(8192)
            file_hash.update(chunk)
        file.close()
        print("Hash Value: ", file_hash.hexdigest())


if __name__ == '__main__':
    # Replace path to required directory in filenames, currently using current directory
    filenames = os.listdir('.')
    for filename in filenames:
        metadata = get_file_metadata(filename)
        print("File Name: ", metadata[0], "\nCreation Date: ", metadata[1],
              "\nLast Edit Date: ", metadata[2], "\nFile Size: ", metadata[3])
        mesh_value(filename)
