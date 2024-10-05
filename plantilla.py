from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

# Función para guardar registros de alumnos en CSV
def guardar_alumno_csv(nombre_alumno, nombre_profesor, pago_alumno):
    with open('alumnos.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nombre_alumno, nombre_profesor, pago_alumno])

# Función para guardar registros de alquileres en CSV
def guardar_alquiler_csv(nombre_alquilador, pago_alquiler):
    with open('alquileres.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nombre_alquilador, pago_alquiler])

# Página principal para ingresar los datos
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar el registro de un alumno
@app.route('/submit_student', methods=['POST'])
def submit_student():
    nombre_alumno = request.form['nombre_alumno']
    nombre_profesor = request.form['nombre_profesor']
    pago_alumno = request.form['pago_alumno']

    # Guardar el alumno en el archivo CSV
    guardar_alumno_csv(nombre_alumno, nombre_profesor, pago_alumno)
    
    return redirect('/')

# Ruta para procesar el registro de un alquiler
@app.route('/submit_rental', methods=['POST'])
def submit_rental():
    nombre_alquilador = request.form['nombre_alquilador']
    pago_alquiler = request.form['pago_alquiler']

    # Guardar el alquiler en el archivo CSV
    guardar_alquiler_csv(nombre_alquilador, pago_alquiler)
    
    return redirect('/')

# Ruta para mostrar el resumen
@app.route('/summary')
def summary():
    # Cargar los datos de los alumnos y alquileres desde los archivos CSV
    profesores = {}
    total_profesores = 0
    alquileres = []
    total_alquileres = 0

    # Leer registros de alumnos
    try:
        with open('alumnos.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                nombre_alumno, nombre_profesor, pago_alumno = row
                pago_alumno = float(pago_alumno)

                # Sumar al total por profesor
                if nombre_profesor in profesores:
                    profesores[nombre_profesor] += pago_alumno
                else:
                    profesores[nombre_profesor] = pago_alumno

                total_profesores += pago_alumno
    except FileNotFoundError:
        pass

    # Leer registros de alquileres
    try:
        with open('alquileres.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                nombre_alquilador, pago_alquiler = row
                pago_alquiler = float(pago_alquiler)
                alquileres.append((nombre_alquilador, pago_alquiler))
                total_alquileres += pago_alquiler
    except FileNotFoundError:
        pass

    # Pasar los datos al template summary.html
    return render_template('summary.html', profesores=profesores, total_profesores=total_profesores, alquileres=alquileres, total_alquileres=total_alquileres)

if __name__ == '__main__':
    app.run(debug=True)
