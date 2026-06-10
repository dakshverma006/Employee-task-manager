from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Employee, Task

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard', methods=['GET'])
@login_required
def index():
    # Employee Stats
    total_employees = Employee.query.filter_by(is_active=True).count()

    # Task Stats
    total_tasks = Task.query.count()
    pending_tasks = Task.query.filter_by(status='Pending').count()
    inprogress_tasks = Task.query.filter_by(status='In Progress').count()
    completed_tasks = Task.query.filter_by(status='Completed').count()

    return render_template('dashboard.html',
        total_employees=total_employees,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        inprogress_tasks=inprogress_tasks,
        completed_tasks=completed_tasks
    )