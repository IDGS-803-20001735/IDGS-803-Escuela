from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Blueprint
import forms
from db import get_connection

blueprint = Blueprint('blueprint',__name__)

maestros = Blueprint('maestros',__name__)

@maestros.route('/getMaestro', methods = ['GET', 'POST'])
def get_maestros():
    maestro_form = forms.MaesForm(request.form)
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call listar_maestro()')
            resulset = cursor.fetchall()
            return render_template('maestros.html', form = maestro_form, resulset = resulset)
    except Exception as ex:
        flash("No se encontro ningún registro en la BD: " + str(ex))
    return render_template('maestros.html', form = maestro_form)

@maestros.route('/insertMaestro', methods = ['GET', 'POST'])
def insert_maestro():
    maestro_form = forms.MaesForm(request.form)
    if request.method == 'POST':
        
        nombre = maestro_form.nombre.data
        apellidos = maestro_form.apellidos.data
        materia = maestro_form.materia.data
        email = maestro_form.email.data

        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call insertar_maestro(%s, %s, %s, %s)', (nombre, apellidos, materia, email))
                connection.commit()
                connection.close()
                flash("El registro se INSERTO satisfactoriamente!")
        except Exception as ex:
            flash("No se pudo INSERTAR el registro: " + str(ex))
        return redirect(url_for('maestros.get_maestros'))
    return render_template('reg_maestros.html', form = maestro_form)

@maestros.route('/updateMaestro', methods = ['GET', 'POST'])
def update_maestro():
    maestro_form = forms.MaesForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        nombre = request.args.get('nombre')
        apellidos = request.args.get('apellidos')
        materia = request.args.get('materia')
        email = request.args.get('email')
        return render_template('update_maestro.html',form = maestro_form, id = id, nombre = nombre, apellidos = apellidos, materia = materia, email = email)
    
    if request.method == 'POST':
        id = maestro_form.id.data
        nombre = maestro_form.nombre.data
        apellidos = maestro_form.apellidos.data
        materia = maestro_form.materia.data
        email = maestro_form.email.data

        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call actualizar_maestro(%s, %s, %s, %s, %s)', (id, nombre, apellidos, materia, email))
                connection.commit()
                connection.close()
                flash("El registro fue ACTUALIZADO satisfactoriamente!")
        except Exception as ex:
            flash("Error al actualizar el registro: " + str(ex))
        return redirect(url_for('maestros.get_maestros'))
    return render_template('update_maestro.html', form = maestro_form)

@maestros.route('/deleteMaestro', methods = ['GET', 'POST'])
def delete_maestro():
    maestro_form = forms.MaesForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        nombre = request.args.get('nombre')
        apellidos = request.args.get('apellidos')
        materia = request.args.get('materia')
        email = request.args.get('email')
        return render_template('delete_maestro.html',form = maestro_form, id = id, nombre = nombre, apellidos = apellidos, materia = materia, email = email)
    
    if request.method == 'POST':
        id = maestro_form.id.data
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call eliminar_maestro(%s)', (id,))
                connection.commit()
                connection.close()
                flash("El registro fue ELIMINADO satisfactoriamente!")
        except Exception as ex:
            flash("Error al ELIMINAR el registro: " + str(ex))
        return redirect(url_for('maestros.get_maestros'))
    return render_template('delete_maestro.html', form = maestro_form)