import os
import sqlite3
import sys

sys.path.append(os.path.abspath(os.path.join('.', '')))
from utils.database import *
import unittest
from utils.check_duplicates import check_duplicates

db_name = "test_firmwaredatabase.db"


def fetch_data():
	db = Database(dbname=db_name)
	if db_name not in os.listdir('.'):
		db.create_table()
	# db connection
	conn = sqlite3.connect(db_name)
	cursor = conn.cursor()
	try:
		cursor.execute("select * from FWDB WHERE Manufacturer='GE'")
	except sqlite3.Error as er:
		print('SQLite error:%s' % (' '.join(er.args)))

	data_list = cursor.fetchall()
	print(data_list)
	conn.close()


class Unit_Case_Test(unittest.TestCase):
	def test_case_db(self):
		db = Database(dbname=db_name)
		if db_name not in os.listdir('.'):
			db.create_table()
		# Create a function for selenium output in dict format and return the dict. Pass it in the next line to insert the data
		data = {
				'Fwfileid': 'file_12345',
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
		}
		db.insert_data(dbdictcarrier=data)
		self.assertTrue(check_duplicates(data, db_name), msg="Data not found in database")
		fetch_data()


if __name__ == "__main__":
	unittest.main()