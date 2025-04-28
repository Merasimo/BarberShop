from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barbershop.db'
db = SQLAlchemy(app)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    customer_phone = db.Column(db.String(20))
    barber_name = db.Column(db.String(100))
    service = db.Column(db.String(100))
    appointment_time = db.Column(db.DateTime)

@app.route('/book', methods=['POST'])
def book_appointment():
    data = request.json
    appointment = Appointment(
        customer_name=data['customer_name'],
        customer_phone=data['customer_phone'],
        barber_name=data['barber_name'],
        service=data['service'],
        appointment_time=datetime.strptime(data['appointment_time'], '%Y-%m-%d %H:%M')
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked successfully!'})

@app.route('/appointments', methods=['GET'])
def list_appointments():
    appointments = Appointment.query.all()
    result = []
    for a in appointments:
        result.append({
            'customer_name': a.customer_name,
            'barber_name': a.barber_name,
            'service': a.service,
            'appointment_time': a.appointment_time.strftime('%Y-%m-%d %H:%M')
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
