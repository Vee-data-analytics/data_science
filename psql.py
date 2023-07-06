import psycopg2
 
conn = psycopg2.connect(host="localhost",
                        database="zibivaxdb",
                        user="zibivaxuser",
                        password="Movuyi90")
 
if conn is not None:
    print('Connection established to PostgreSQL.')
else:
    print('Connection not established to PostgreSQL.')

