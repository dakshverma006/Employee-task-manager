from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Employee, User
from app import db, bcrypt

employees = Blueprint('employees', __name__)

# ─── View All Employees ───────────────────────
@employees.route('/employees')
@login_required
def index():
    all_employees = Employee.query.filter_by(is_active=True).all()
    return render_template('employees/index.html', employees=all_employees)

# ─── Add Employee ─────────────────────────────
@employees.route('/employees/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        designation = request.form.get('designation')
        password = request.form.get('password')

        # Create Employee
        employee = Employee(
            name=name,
            email=email,
            phone=phone,
            address=address,
            designation=designation
        )
        db.session.add(employee)

        # Create User account for employee
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(
            name=name,
            email=email,
            password=hashed_pw,
            role='employee'
        )
        db.session.add(user)
        db.session.commit()

        flash('Employee added successfully!', 'success')
        return redirect(url_for('employees.index'))

    return render_template('employees/add.html')

# ─── Edit Employee ────────────────────────────
@employees.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.name = request.form.get('name')
        employee.email = request.form.get('email')
        employee.phone = request.form.get('phone')
        employee.address = request.form.get('address')
        employee.designation = request.form.get('designation')
        db.session.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('employees.index'))
    return render_template('employees/edit.html', employee=employee)

# ─── Delete Employee ──────────────────────────
@employees.route('/employees/delete/<int:id>')
@login_required
def delete(id):
    employee = Employee.query.get_or_404(id)
    employee.is_active = False
    db.session.commit()
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('employees.index'))