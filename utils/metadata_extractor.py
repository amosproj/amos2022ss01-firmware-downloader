import hashlib
import os
import time


def get_file_metadata(file_path):
    # It will return the properties of the file by using file path
    file_name = os.path.basename(file_path)
    creation_date = time.ctime(os.path.getctime(file_path))
    last_edit_date = time.ctime(os.path.getmtime(file_path))
    file_size = os.path.getsize(file_path)
    return file_name, creation_date, last_edit_date, file_size


def get_hash_value(file_path):
    # Returns the hash value of the file using file path
    with open(file_path, "rb") as file:
        file_hash = hashlib.sha512()
        # file_hash read as sha512 encryption format
        if file.read(file_hash.block_size):
            chunk = file.read(file_hash.block_size)
            # file is read at a speed of file_hash.block_size and updates the new value in file_hash
            file_hash.update(chunk)
        return file_hash.hexdigest()


def metadata_extractor(file_path):
    # Returns metadata of the file using file path in dictionary
    metadata = get_file_metadata(file_path)
    hash_value = get_hash_value(file_path)
    properties = {"File Name": metadata[0], "Creation Date": metadata[1], "Last Edit Date": metadata[2],
                  "File Size": str(metadata[3]) + ' bytes', "Hash Value": hash_value}
    return properties
