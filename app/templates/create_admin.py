from app import create_app, db, bcrypt
from app.models import User

app = create_app()

with app.app_context():
    hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
    admin = User(name='Admin', email='admin@test.com', password=hashed_pw, role='admin')
    db.session.add(admin)
    db.session.commit()
    print("Admin created successfully!")