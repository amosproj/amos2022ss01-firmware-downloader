import sqlite3
from utils.Logs import get_logger
logger = get_logger("utils.database")


# The Database class is defined to maintain the db functionalities like create_table, insert_table
class Database:

	def __init__(self, dbname):
		# The initialization function is available for all the methods with the db name
		self.dbname = dbname
		self.dbdict = {
			'Fwfileid': '',
			'Fwfilename': '',
			'Manufacturer': '',
			'Modelname': '',
			'Version': '',
			'Type': '',
			'Releasedate': '',
			'Checksum': '',
			'Embatested': '',
			'Embalinktoreport': '',
			'Embarklinktoreport': '',
			'Fwdownlink': '',
			'Fwfilelinktolocal': '',
			'Fwadddata': ''
		}

	def create_table(self):
		""" The create_table functions connects to the db: firmwaredatabase if db is not available in the repo
		and if db is available it will carry the tasks like insert.
		A new functionality check need to be configured inorder to avoid multiple datasets for same data.
		The execute command in create_table fn will be used if table FWDB is not present in the file"""
		conn = sqlite3.connect(self.dbname)
		curs = conn.cursor()
		logger.info(f'As there is no db local file, a new {self.dbname} will be created in the file directory.')
		create_command = """CREATE TABLE IF NOT EXISTS FWDB(
						Fwfileid VARCHAR PRIMARY KEY,
						Fwfilename VARCHAR NOT NULL,
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
						Fwadddata BLOB)"""
		curs.execute(create_command)
		logger.info(f'The database is created successfully in the code repository with the command {create_command}.')
		conn.commit()
		curs.close()

	def insert_data(self, dbdictcarrier):
		try:
			"""The insert_data function is used to update the new data in the db with 
			dbdictcarrier as an dictionary input"""
			logger.debug(f'As the {self.dbname} is found, a new connection will be established.')
			conn = sqlite3.connect(self.dbname)
			logger.debug('Connection details: {}'.format(conn))
			curs = conn.cursor()
			logger.debug(f'A cursor is established on {self.dbname}, with the details {curs}.')
			select_command = "select * from FWDB"
			curs.execute(select_command)
			logger.debug(f'The table FWDB is selected in the {self.dbname} with the command: {select_command}.')
			records = len(curs.fetchall())
			dbdict = self.dbdict
			for key in dbdict:
				dbdict[key] = dbdictcarrier[key]
				logger.debug(f'The {self.dbname} is updated with the Key: {key} and Value: {dbdict[key]}.')
			dbdict['Fwfileid'] = f'FILE_{records + 1}'
			logger.debug(f"The db is updated with the Fwfileid. as {dbdict['Fwfileid']}.")
			# Currently, the local firmware id is represented as file extended by _ in increase by 1
			insert_command = f'''INSERT INTO FWDB('{"','".join(map(str, dbdict.keys()))}') 
			VALUES('{"','".join(map(str, dbdict.values()))}')'''
			curs.execute(insert_command)
			logger.debug(f'The db is inserted with the command {insert_command}.')
			conn.commit()
			logger.debug(f'The db commited is with data {dbdict}.')
			# Prints the data in db
			curs.execute('SELECT * FROM FWDB')
			print(curs.fetchall())
			curs.close()
		except Exception as error:
			logger.error(f"Error writing to db {dbdictcarrier}")
			print(error)
