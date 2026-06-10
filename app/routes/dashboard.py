from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Employee, Task

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard', methods=['GET'])
@login_required
def index():
    if current_user.role == 'admin':
        # Admin sees full stats
        total_employees = Employee.query.filter_by(is_active=True).count()
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
    else:
        # Employee sees only their tasks
        employee = Employee.query.filter_by(email=current_user.email).first()
        my_tasks = Task.query.filter_by(assigned_to=employee.id).all() if employee else []
        return render_template('employee_dashboard.html', my_tasks=my_tasks)