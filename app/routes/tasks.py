from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Task, Employee
from app import db
from datetime import datetime

tasks = Blueprint('tasks', __name__)

# ─── View All Tasks ───────────────────────────
@tasks.route('/tasks')
@login_required
def index():
    all_tasks = Task.query.all()
    return render_template('tasks/index.html', tasks=all_tasks)

# ─── Create Task ──────────────────────────────
@tasks.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add():
    employees = Employee.query.filter_by(is_active=True).all()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        due_date = request.form.get('due_date')
        assigned_to = request.form.get('assigned_to')

        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=datetime.strptime(due_date, '%Y-%m-%d') if due_date else None,
            assigned_to=int(assigned_to) if assigned_to else None,
            status='Pending'
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks.index'))

    return render_template('tasks/add.html', employees=employees)

# ─── Edit Task ────────────────────────────────
@tasks.route('/tasks/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    task = Task.query.get_or_404(id)
    employees = Employee.query.filter_by(is_active=True).all()
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.priority = request.form.get('priority')
        task.assigned_to = request.form.get('assigned_to')
        due_date = request.form.get('due_date')
        task.due_date = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks.index'))
    return render_template('tasks/edit.html', task=task, employees=employees)

# ─── Update Task Status ───────────────────────
@tasks.route('/tasks/status/<int:id>', methods=['POST'])
@login_required
def update_status(id):
    task = Task.query.get_or_404(id)
    task.status = request.form.get('status')
    db.session.commit()
    flash('Task status updated!', 'success')
    return redirect(url_for('tasks.index'))

# ─── Delete Task ──────────────────────────────
@tasks.route('/tasks/delete/<int:id>')
@login_required
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks.index'))