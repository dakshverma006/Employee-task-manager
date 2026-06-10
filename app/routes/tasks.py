from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Task, Employee
from app import db
from datetime import datetime
from app.email_helper import send_email

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

        # ─── Send Email Notification ──────────
        if assigned_to:
            employee = Employee.query.get(int(assigned_to))
            if employee:
                send_email(
                    to_email=employee.email,
                    subject='New Task Assigned to You',
                    body=f'''
                    <div style="font-family:Segoe UI,sans-serif;max-width:500px;margin:auto;padding:30px;border-radius:16px;background:linear-gradient(135deg,#667eea,#764ba2);">
                        <h2 style="color:white;">📋 New Task Assigned!</h2>
                        <div style="background:white;border-radius:12px;padding:25px;margin-top:20px;">
                            <p>Hi <strong>{employee.name}</strong>,</p>
                            <p>You have been assigned a new task:</p>
                            <table style="width:100%;border-collapse:collapse;margin-top:15px;">
                                <tr style="background:#f8f7ff;">
                                    <td style="padding:10px;font-weight:600;">Task</td>
                                    <td style="padding:10px;">{title}</td>
                                </tr>
                                <tr>
                                    <td style="padding:10px;font-weight:600;">Description</td>
                                    <td style="padding:10px;">{description or "N/A"}</td>
                                </tr>
                                <tr style="background:#f8f7ff;">
                                    <td style="padding:10px;font-weight:600;">Priority</td>
                                    <td style="padding:10px;">{priority}</td>
                                </tr>
                                <tr>
                                    <td style="padding:10px;font-weight:600;">Due Date</td>
                                    <td style="padding:10px;">{due_date or "N/A"}</td>
                                </tr>
                            </table>
                            <p style="margin-top:20px;color:#888;">Please login to your dashboard to view and update this task.</p>
                        </div>
                    </div>
                    '''
                )
                flash(f'Task assigned and email sent to {employee.name}!', 'success')
        else:
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
        new_assigned_to = request.form.get('assigned_to')
        due_date = request.form.get('due_date')
        task.due_date = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None

        # ─── Send email if employee changed ───
        if new_assigned_to and int(new_assigned_to) != task.assigned_to:
            employee = Employee.query.get(int(new_assigned_to))
            if employee:
                send_email(
                    to_email=employee.email,
                    subject='Task Assigned to You',
                    body=f'''
                    <div style="font-family:Segoe UI,sans-serif;max-width:500px;margin:auto;padding:30px;border-radius:16px;background:linear-gradient(135deg,#667eea,#764ba2);">
                        <h2 style="color:white;">📋 Task Assigned!</h2>
                        <div style="background:white;border-radius:12px;padding:25px;margin-top:20px;">
                            <p>Hi <strong>{employee.name}</strong>,</p>
                            <p>A task has been assigned to you:</p>
                            <table style="width:100%;border-collapse:collapse;margin-top:15px;">
                                <tr style="background:#f8f7ff;">
                                    <td style="padding:10px;font-weight:600;">Task</td>
                                    <td style="padding:10px;">{task.title}</td>
                                </tr>
                                <tr>
                                    <td style="padding:10px;font-weight:600;">Priority</td>
                                    <td style="padding:10px;">{task.priority}</td>
                                </tr>
                                <tr style="background:#f8f7ff;">
                                    <td style="padding:10px;font-weight:600;">Due Date</td>
                                    <td style="padding:10px;">{due_date or "N/A"}</td>
                                </tr>
                            </table>
                            <p style="margin-top:20px;color:#888;">Please login to your dashboard to view and update this task.</p>
                        </div>
                    </div>
                    '''
                )
                flash(f'Task updated and email sent to {employee.name}!', 'success')

        task.assigned_to = int(new_assigned_to) if new_assigned_to else None
        db.session.commit()
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
    return redirect(url_for('dashboard.index'))

# ─── Delete Task ──────────────────────────────
@tasks.route('/tasks/delete/<int:id>')
@login_required
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks.index'))