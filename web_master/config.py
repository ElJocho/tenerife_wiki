import os
user = os.getenv('POSTGRES_USER', "tenerife_db")
password = os.getenv('POSTGRES_PASSWORD', "basaltic")
host = os.getenv('POSTGRES_HOST', "localhost")
database = os.getenv('POSTGRES_DB', "tenerife_db")
port = os.getenv('POSTGRES_PORT', 5446)
superuser_pw = os.getenv('SUPERUSER_PW', "Valid12!")
DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
