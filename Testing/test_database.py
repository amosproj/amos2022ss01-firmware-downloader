from database import Database
import os

db_name = 'firmwaredatabase.db'
db = Database(dbname=db_name)
if db_name not in os.listdir('.'):
	db.create_table()
# Create a function for selenium output in dict format and return the dict. Pass it in the next line to insert the data
db.insert_data(dbdictcarrier={
		'Fwfileid': 'FILE',
		'Manufacturer': 'Siemens',
		'Modelname': 'SZ-100',
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
	})
