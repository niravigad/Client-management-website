from flask import Blueprint, render_template, request, flash, redirect, url_for
import ipaddress
from . import db
from .models import User

auth = Blueprint('auth', __name__)


# this route is for inserting data to mysql database via html forms

@auth.route('/', methods=['GET', 'POST'])
def index():
    all_data = User.query.all()
    return render_template("home.html", employees=all_data)


@auth.route('/', methods=['GET', 'POST'])
def search():
    my_search = User.query.get(request.form.get('to_search'))
    exists = db.session.query(db.exists().where(User.Teudat_Zehut == my_search.Teudat_Zehut)).scalar()
    if exists:
        flash('Test', category='error')
        return render_template("home.html", employees=exists)
    else:
        flash('Teudat_Zehut not exist', category='error')


# this is our update route where we are going to update our employee
@auth.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = User.query.get(request.form.get('id'))

        my_data.name = request.form.get('name')
        my_data.ip_address = request.form.get('ip_address')
        my_data.Teudat_Zehut = request.form.get('Teudat_Zehut')
        my_data.phone = request.form.get('phone')
        exists = db.session.query(db.exists().where(User.Teudat_Zehut == my_data.Teudat_Zehut)).scalar()
        if exists:
            flash('Teudat_Zehut is already taken', category='error')
            return redirect(url_for('auth.index'))

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('auth.index'))


# This route is for deleting our employee
@auth.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('auth.index'))


@auth.route('/insert', methods=['POST'])
def add_new_client():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        ip_address = request.form.get('ip_address')
        Teudat_Zehut = request.form.get('Teudat_Zehut')
        exists = db.session.query(db.exists().where(User.Teudat_Zehut == Teudat_Zehut)).scalar()
        error = False
# syntax check of the values :
        if exists:
            flash('Teudat_Zehut is already taken', category='error')
            error = True
            return redirect(url_for('auth.index'))
        elif len(Teudat_Zehut) != 9:
            flash('Teudat_Zehut must be 9 characters exactly .', category='error')
            error = True
        elif len(name) < 1:
            flash('name must be greater than 1 characters.', category='error')
            error = True
        elif not phone.startswith('+972-'):
            flash('phone must start with state code , for example +972-52.. ', category='error')
            error = True
        try:
            ip = ipaddress.ip_address(ip_address)
        except ValueError:
            flash('Invalid ip address', category='error')
            error = True

        if not error:
            new_client = User(name=name, ip_address=ip_address, Teudat_Zehut=Teudat_Zehut, phone=phone)
            db.session.add(new_client)
            db.session.commit()
            flash('Client has been added !', category='success')
        return redirect(url_for('auth.index'))

    elif request.method == 'GET':
        all_data = User.query.all()
        return render_template("home.html", employees=all_data)



