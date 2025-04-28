from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Create Flask app
app = Flask(__name__)

# Configure database (using SQLite for now)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database object
db = SQLAlchemy(app)

# Define Appointment model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return "Welcome to the Barbershop Appointment API!"

@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    new_appointment = Appointment(name=data['name'], time=data['time'])
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment created!'}), 201

@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    output = []
    for appointment in appointments:
        output.append({'name': appointment.name, 'time': appointment.time})
    return jsonify(output)

# Run locally if needed
if __name__ == '__main__':
    app.run(debug=True)
