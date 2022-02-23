from turtle import title
from server import app, db
from flask import render_template, redirect, url_for, flash, get_flashed_messages
import forms
from datetime import datetime
from models import Task

@app.route('/')
@app.route('/index')
def index():
    tasks = Task.query.all()
    return render_template('index.html', current_title = 'Custom Title', tasks = tasks)


@app.route('/add', methods = ['POST', 'GET'])
def add():
    form = forms.AddTaskForm()
    if form.validate_on_submit():
        t = Task(title = form.title.data, date= datetime.utcnow())
        db.session.add(t)
        db.session.commit()
        print('submitted tittle', form.title.data)
        flash('task added to data base!')
        return redirect(url_for('index'))
    return render_template('add.html', form = form)


@app.route('/edit/<int:task_id>', methods = ['POST', 'GET'])
def edit(task_id):
    task = Task.query.get(task_id)
    form = forms.AddTaskForm()
    if task:
        if form.validate_on_submit():
            task.title = form.title.data
            task.date = datetime.utcnow()
            db.session.commit()
            flash('has been updated!')
            return redirect(url_for('index'))
        form.title.data = task.title
        return render_template('edit.html', form = form, task_id = task_id)
    else:
        flash('Task not found!')
    print(task)
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>', methods = ['POST', 'GET'])
def delete(task_id):
    task = Task.query.get(task_id)
    form = forms.DeleteTaskForm()
    if task:
        if form.validate_on_submit():
            db.session.delete(task)
            db.session.commit()
            flash('has been deleted!')
            return redirect(url_for('index'))
        return render_template('delete.html', form = form, task_id = task_id, title = task.title)
    else:
        flash('Not Found')
    return redirect(url_for('index'))