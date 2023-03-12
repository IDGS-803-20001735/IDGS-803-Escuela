from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Blueprint
import forms
from db import get_connection

blueprint = Blueprint('blueprint',__name__)

alumnos = Blueprint('alumnos',__name__)

@alumnos.route('/getAlumno', methods = ['GET', 'POST'])
def get_alumnos():
    alumno_form = forms.AlumnForm(request.form)
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call listar_alumno()')
            resulset = cursor.fetchall()
            return render_template('alumnos.html', form = alumno_form, resulset = resulset)
    
    except Exception as ex:
        print(ex)

@alumnos.route('/insertAlumno', methods = ['GET', 'POST'])
def insert_alumno():
    alumno_form = forms.AlumnForm(request.form)
    if request.method == 'POST':
        nombre = alumno_form.nombre.data
        apellidos = alumno_form.apellidos.data
        grupo = alumno_form.grupo.data
        email = alumno_form.email.data

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call insertar_alumno(%s, %s, %s, %s)', (nombre, apellidos, grupo, email))
                connection.commit()
                connection.close()
                flash("Registro ALMACENADO satisfactoriamente")
        except Exception as ex:
            flash("No fue posible insertar el registro: " + str(ex))
        return redirect(url_for('alumnos.get_alumnos'))
    
    return render_template('reg_alumnos.html', form = alumno_form)

@alumnos.route('/updateAlumno', methods = ['GET', 'POST'])
def update_alumno():
    alumno_form = forms.AlumnForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        nombre = request.args.get('nombre')
        apellidos = request.args.get('apellidos')
        grupo = request.args.get('grupo')
        email = request.args.get('email')

        return render_template('update_alumnos.html', form = alumno_form, id = id, nombre = nombre, apellidos = apellidos, grupo = grupo, email = email)

    if request.method == 'POST':
        id = alumno_form.id.data
        nombre = alumno_form.nombre.data
        apellidos = alumno_form.apellidos.data
        grupo = alumno_form.grupo.data
        email = alumno_form.email.data

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call actualizar_alumno(%s, %s, %s, %s, %s)', (id, nombre,apellidos, grupo, email))
                connection.commit()
                connection.close()
                flash("Registro ATUALIZADO satisfactoriamente")
        except Exception as ex:
            flash("No fue posible actualizar el registro: " + str(ex))
        return redirect(url_for('alumnos.get_alumnos'))
    
    return render_template('update_alumnos.html', form = alumno_form)

@alumnos.route('/deleteAlumno', methods = ['GET', 'POST'])
def delete_alumno():
    alumno_form = forms.AlumnForm(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        nombre = request.args.get('nombre')
        apellidos = request.args.get('apellidos')
        grupo = request.args.get('grupo')
        email = request.args.get('email')

        return render_template('delete_alumnos.html', form = alumno_form, id = id, nombre = nombre, apellidos = apellidos, grupo = grupo, email = email)
    
    if request.method == 'POST':
        id = alumno_form.id.data
        
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call eliminar_alumno(%s)', (id,))
                connection.commit()
                connection.close()

                flash("Registro ELIMINADO satisfactoriamente")
        except Exception as ex:
            flash("No fue posible eliminar el registro: " + str(ex))
        return redirect(url_for('alumnos.get_alumnos'))
    
    return render_template('delete_alumnos.html', form = alumno_form)

@alumnos.route('/searchAlumno', methods = ['POST'])
def search_alumno():
    alumno_form = forms.AlumnForm(request.form)
    buscar = request.form.get('buscar')

    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call buscar_alumno(%s)',(buscar,))
            resulset = cursor.fetchall()
            return render_template('alumnos.html', form = alumno_form, resulset = resulset)
    except Exception as ex:
        flash("No fue posible encotrar el registro: " + str(ex))