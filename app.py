import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://flask:flask@db/flask'
app.config['SQLALCHEMY_MIGRATE_REPO'] = os.path.join(basedir, 'db_repository')

db = SQLAlchemy(app)


class Departments(db.Model):
    name = ''
    status = False
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    status = db.Column(db.Boolean, index=False, unique=False)

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def __repr__(self):
        return ' ' % (self.name)


class Positions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    description = db.Column(db.String(), index=True, unique=True)
    status = db.Column(db.Boolean)

    def __init__(self, name, description, status):
        self.name = name
        self.description = description
        self.status = status

    def __repr__(self):
        return ' ' % (self.name)
@app.route('/')
def homepage():
    return 'Wellcome'

@app.route('/departments', methods = ['POST', 'GET'])
def departments():
    departs = Departments.query.all()
    return render_template('index.html', departs=departs)

@app.route('/departments/create')
def createDepartment():
    return render_template('departments/create.html')

@app.route('/departments/store', methods = ['POST', 'GET'])
def storeDepartment():
    if request.method == 'POST':
        model = Departments(request.form['name'], 1 if ('status' in request.form) else 0)
        db.session.add(model)
        db.session.commit()
        return redirect(url_for('departments'))
    return render_template('departments/create.html')

@app.route('/departments/edit/<depart_id>', methods = ['GET'])
def editDepartment(depart_id):
    depart = Departments.query.filter_by(id=depart_id).first()
    if depart is not None:
        return render_template('departments/edit.html', depart=depart)
    else:
        return render_template('404.html')

@app.route('/departments/update/<depart_id>', methods = ['POST', 'GET'])
def updateDepartment(depart_id):
    name = request.form['name']
    status = 1 if ('status' in request.form) else 0
    Departments.query.filter_by(id=depart_id).update(dict(name=name, status=status))
    db.session.commit()
    return redirect(url_for('departments'))

@app.route('/departments/delete/<depart_id>', methods = ['POST', 'GET'])
def deleteDepartment(depart_id):
    depart = Departments.query.filter_by(id=depart_id).first()
    if depart is not None:
        depart.delete()
        # db.session.delete(Departments(depart['id'], depart['name'], depart['status']))
        db.session.commit()
        return redirect(url_for('departments'))
    else:
        return render_template('404.html')

@app.route('/migrate')
def migrate():
    db.create_all()
    db.session.commit()
    return 'hello'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)