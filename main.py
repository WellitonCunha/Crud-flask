import psycopg2
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="python",host="localhost",user="postgres",password="root",port="5432")
    return conn

@app.route('/api/resources', methods=['GET'])
def list_resources():
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM CASA ORDER BY ID ASC''')
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/create', methods=['POST'])
def create_resource():
    new_resource = request.get_json()
    conn = db_conn()
    cursor = conn.cursor()
    nome = new_resource["nome"]
    cursor.execute('''INSERT INTO CASA (nome) VALUES (%s)''',(nome,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Recurso criado com sucesso"})

@app.route('/api/update/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    update_data = request.get_json()  
    nome = update_data.get("nome")
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute('''UPDATE CASA SET nome=%s WHERE id=%s''',(nome,resource_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Recurso atualizado com sucesso"})

@app.route('/api/delete/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM CASA WHERE id=%s''',(resource_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Registro deletado com sucesso"})
#-------------------------------------------------------------------------
@app.route('/')
def index():
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM CASA ORDER BY ID ASC''')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html',data=data)

@app.route('/create', methods=['POST'])
def create():
    conn = db_conn()
    cursor = conn.cursor()
    nome = request.form['nome']
    cursor.execute('''INSERT INTO CASA (nome) VALUES (%s)''',(nome,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    conn = db_conn()
    cursor = conn.cursor()
    nome = request.form['nome']
    id = request.form['id']
    cursor.execute('''UPDATE CASA SET nome=%s WHERE id=%s''',(nome,id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    conn = db_conn()
    cursor = conn.cursor()
    id = request.form['id']
    cursor.execute('''DELETE FROM CASA WHERE id=%s''',(id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

app.run()