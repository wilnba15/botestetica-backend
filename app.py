
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('citas.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            fecha TEXT,
            hora TEXT,
            tratamiento TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/guardar-cita', methods=['POST'])
def guardar_cita():
    data = request.get_json()
    nombre = data.get('nombre')
    fecha = data.get('fecha')
    hora = data.get('hora')
    tratamiento = data.get('tratamiento')

    conn = sqlite3.connect('citas.db')
    c = conn.cursor()
    c.execute('INSERT INTO citas (nombre, fecha, hora, tratamiento) VALUES (?, ?, ?, ?)',
              (nombre, fecha, hora, tratamiento))
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Cita registrada exitosamente"}), 200

@app.route('/ver-citas', methods=['GET'])
def ver_citas():
    conn = sqlite3.connect('citas.db')
    c = conn.cursor()
    c.execute('SELECT nombre, fecha, hora, tratamiento FROM citas ORDER BY fecha ASC, hora ASC')
    citas = [
        {"nombre": row[0], "fecha": row[1], "hora": row[2], "tratamiento": row[3]}
        for row in c.fetchall()
    ]
    conn.close()
    return jsonify(citas)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
