import psycopg2

conn = psycopg2.connect(database="python",host="localhost",user="postgres",password="root",port="5432")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE CASA (ID SERIAL PRIMARY KEY, NOME VARCHAR);''')
cursor.execute('''INSERT INTO CASA (NOME) VALUES ('1'),('2'),('3');''')

conn.commit()
cursor.close()
conn.close()