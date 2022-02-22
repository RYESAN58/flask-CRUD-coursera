from server import app, db
from flask import render_template, redirect, url_for
import forms
from models import Task
from datetime import datetime

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', current_title = 'Custom Title' , tasks = tasks )


@app.route('/about', methods = ['POST', 'GET'])
def about():
    form = forms.AddTaskForm()
    if form.validate_on_submit():
        t = Task(title = form.title.data, date= datetime.utcnow())
        db.session.add(t)
        #db.session.commit()
        print('submitted tittle', form.title.data)
        return redirect(url_for('index'))
    return render_template('about.html', form = form)

