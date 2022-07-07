import os
import sys

sys.path.append(os.path.abspath(os.path.join('.', '')))
from utils.database import Database


db_name = 'firmwaredatabase.db'
db = Database()
# if db_name not in os.listdir('.'):
# 	db.create_table()
# Create a function for selenium output in dict format and return the dict. Pass it in the next line to insert the data
db.insert_data(dbdictcarrier={
		'Fwfileid': 'FILE',
		'Fwfilename': 'Siemens ABC firmware',
		'Manufacturer': 'Siemens',
		'Modelname': 'SZ-100',
		'Version': '1.2.3',
		'Type': 'Router',
		'Releasedate': '2022-05-31',
		'Checksum': 'None',
		'Embatested': 'Yes',
		'Embalinktoreport': 'None',
		'Embarklinktoreport': 'https://xyz.com',
		'Fwdownlink': 'https://google.com',
		'Fwfilelinktolocal': './xyz/abc.tar',
		'Fwadddata': 'some long sentence'
	})
