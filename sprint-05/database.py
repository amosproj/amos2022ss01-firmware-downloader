import sqlite3, logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
file_handler = logging.FileHandler('db.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# The Database class is defined to maintain the db functionalities like create_table, insert_table
class Database:

	def __init__(self, dbname):
		# The initialization function is available for all the methods with the db name
		self.dbname = dbname
		self.dbdict = {
			'Fwfileid': '',
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
		logger.info(
			'As there is no db local file, a new {} will be created in the file directory.'.format(self.dbname))
		create_command = """CREATE TABLE IF NOT EXISTS FWDB(
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
						Fwadddata BLOB)"""
		curs.execute(create_command)
		logger.info(
			'The database is created successfully in the code repository with the command {}.'.format(create_command))
		conn.commit()
		curs.close()

	def insert_data(self, dbdictcarrier):
		# The insert_data function is used to update the new data in the db with dbdictcarrier as an dictionary input
		logger.info('As the {} is found, a new connection will be established.'.format(self.dbname))
		conn = sqlite3.connect(self.dbname)
		logger.info('Connection details: {}'.format(conn))
		curs = conn.cursor()
		logger.info('A cursor is established on {}, with the details {}.'.format(self.dbname, curs))
		select_command = "select * from FWDB"
		curs.execute(select_command)
		logger.info('The table FWDB is selected in the {} with the command: {}.'.format(self.dbname, select_command))
		records = len(curs.fetchall())
		dbdict = self.dbdict
		for key in dbdict:
			dbdict[key] = dbdictcarrier[key]
			logger.info('The {} is updated with the Key: {} and Value: {}.'.format(self.dbname, key, dbdict[key]))
		dbdict['Fwfileid'] = f'FILE_{records + 1}'
		logger.info('The db is updated with the Fwfiledid.')
		# Currently, the local firmware id is represented as file extended by _ in increase by 1
		insert_command = f'''INSERT INTO FWDB('{"','".join(map(str, dbdict.keys()))}') 
									VALUES('{"','".join(map(str, dbdict.values()))}')'''
		curs.execute(insert_command)
		logger.info('The db is inserted with the command {}.'.format(insert_command))
		conn.commit()
		logger.info('The db commited is with data {}.'.format(dbdict))
		# Prints the data in db
		curs.execute('SELECT * FROM FWDB')
		print(curs.fetchall())
		curs.close()
