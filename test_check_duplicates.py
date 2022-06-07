from check_duplicates import check_duplicates

temp_data = {
    'Fwfileid': 'FILE',
    'Manufacturer': 'GE',
    'Modelname': 'orbit-bkrc-9_2_2.mpk',
    'Version': '',
    'Type': '',
    'Releasedate': '2022-05-31',
    'Checksum': 'None',
    'Embatested': 'Yes',
    'Embalinktoreport': 'None',
    'Embarklinktoreport': 'https://xyz.com',
    'Fwdownlink': 'https://google.com',
    'Fwfilelinktolocal': './xyz/abc.tar',
    'Fwadddata': 'some long sentence'
}

if __name__ == "__main__":
    if(check_duplicates(temp_data)):
        print("Data already exist")
    else:
        print("Data not exist")
