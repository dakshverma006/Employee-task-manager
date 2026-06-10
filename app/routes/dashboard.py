from flask import Blueprint, render_template
from flask_login import login_required

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard', methods=['GET'])
@login_required
def index():
    return render_template('dashboard.html')