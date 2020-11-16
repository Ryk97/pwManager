import psycopg2
import sys

class DatabaseManager:
    
    def __init__(self, configuration=None):
            with open(configuration.db.db_env_path) as f:
                lines = f.readlines()
            credentials_dict = dict()
            for line in lines:
                key = line.split('=')[0]
                value = line.split('=')[1].strip('\n')
                credentials_dict[key] = value
            if not ('POSTGRES_USER' and 'POSTGRES_PASSWORD' in credentials_dict.keys()):
                print('There are no credentials in your db.env file to connect to the database!')
                sys.exit(1)
            self.db_username = credentials_dict['POSTGRES_USER']
            self.db_password = credentials_dict['POSTGRES_PASSWORD']
            if configuration.db is not None:
                self.db_connection_conf = configuration.db
            else: 
                print('No database configuration found. Using fallback values.')
                self.db_host = '127.0.0.1'
                self.db_port = 8080
            self.initialize()
    
    def connect(self):
        try:
            connection = psycopg2.connect(user=self.db_username, password=self.db_password, host=self.db_connection_conf.db_host, port=self.db_connection_conf.db_port, database=self.db_username)
            return connection
        except (Exception, psycopg2.Error) as error:
            print(error)

    def initialize(self):
        connection = self.connect()
        cursor = connection.cursor()
        accounts_table_initialization_query = """
            CREATE TABLE IF NOT EXISTS accounts (
                password VARCHAR(255),
                email VARCHAR(255),
                username VARCHAR(255),
                url VARCHAR(255),
                app_name VARCHAR(255)
            )
        """
        cursor.execute(accounts_table_initialization_query)
        connection.commit()

    def store_password(self, password, user_email, username, url, app_name):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            postgres_insert_query = """ INSERT INTO accounts (password, email, username, url, app_name) VALUES (%s, %s, %s, %s, %s)"""
            record_to_insert = (password, user_email, username, url, app_name)
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
        except (Exception, psycopg2.Error) as error:
            print(error)

    def find_password(self, app_name):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            postgres_select_query = """ SELECT password FROM accounts WHERE app_name = '""" + app_name + "'"
            cursor.execute(postgres_select_query, app_name)
            connection.commit()
            result = cursor.fetchone()
            print('Password is: ' )
            print(result[0])
        
        except (Exception, psycopg2.Error) as error:
            print(error)

    def find_users(self, user_email):
        data = ('Password: ', 'Email: ', 'Username: ', 'url: ', 'App/Site name: ') 
        try:
            connection = self.connect()
            cursor = connection.cursor()
            postgres_select_query = """ SELECT * FROM accounts WHERE email = '""" + user_email + "'"
            cursor.execute(postgres_select_query, user_email)
            connection.commit()
            result = cursor.fetchall()
            print('')
            print('RESULT')
            print('')
            for row in result:
                for i in range(0, len(row)-1):
                    print(data[i] + row[i])
            print('')
            print('-'*30)
        except (Exception, psycopg2.Error) as error:
            print(error)
