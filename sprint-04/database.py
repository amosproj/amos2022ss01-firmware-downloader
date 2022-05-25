import sqlite3, os, logging

logging.basicConfig(filename='db.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


# The Database class is defined to maintain the db functionalities like create_table, insert_table
class Database:

	def __init__(self, dbname):
		# The initialization function is available for all the methods with the db name
		self.dbname = dbname

	def create_table(self):
		""" The create_table functions connects to the db: firmwaredatabase if db is not available in the repo
		and if db is available it will carry the tasks like insert.
		A new functionality check need to be configured inorder to avoid multiple datasets for same data.
		The execute command in create_table fn will be used if table FWDB is not present in the file"""
		conn = sqlite3.connect(self.dbname)
		curs = conn.cursor()
		curs.execute("""CREATE TABLE IF NOT EXISTS FWDB(
						Fwfileid VARCHAR PRIMARY KEY,
						Manufacturer TEXT NOT NULL,
						Modelname VARCHAR NOT NULL,
						Version TEXT NOT NULL,
						Type TEXT NOT NULL,
						Releasedate TEXT,
						Checksum TEXT,
						Embatested TEXT NOT NULL,
						Embalinktoreport TEXT,
						Embarklinktoreport TEXT,
						Fwdownlink TEXT NOT NULL,
						Fwfilelinktolocal TEXT NOT NULL,
						Fwadddata BLOB)""")
		conn.commit()
		curs.close()

	def insert_data(self, dbdict=None):
		# The insert_data function is used to update the new data in the db
		conn = sqlite3.connect(self.dbname)
		curs = conn.cursor()
		curs.execute("select * from FWDB")
		records = len(curs.fetchall())
		# Remove the below once dbdict comes as an input. Below is for test purpose
		dbdict = {
			'Fwfileid': 'FILE',
			'Manufacturer': 'Siemens',
			'Modelname': 'SZ-100',
			'Version': '1.2.3',
			'Type': 'Router',
			'Releasedate': '2022-05-24',
			'Checksum': 'None',
			'Embatested': 'Yes',
			'Embalinktoreport': 'None',
			'Embarklinktoreport': 'https://xyz.com',
			'Fwdownlink': 'https://google.com',
			'Fwfilelinktolocal': './xyz/abc.tar',
			'Fwadddata': 'some long sentence'
		}
		dbdict['Fwfileid'] = f'FILE_{records + 1}'
		# Currently, the local firmware id is represented as file extended by _ in increase by 1
		command = f'''INSERT INTO FWDB('{"','".join(map(str, dbdict.keys()))}') 
									VALUES('{"','".join(map(str, dbdict.values()))}')'''
		curs.execute(command)
		conn.commit()
		# Prints the data in db
		curs.execute('SELECT * FROM FWDB')
		print(curs.fetchall())
		curs.close()


if __name__ == '__main__':
	db_name = 'firmwaredatabase.db'
	db = Database(dbname=db_name)
	if db_name not in os.listdir('.'):
		db.create_table()
	# Create a function for selenium output in dict format and return the dict. Pass it in the next line to insert the data
	db.insert_data(dbdict=None)
