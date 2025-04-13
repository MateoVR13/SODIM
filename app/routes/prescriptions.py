from flask import Blueprint, request, jsonify
from app import db
from app.models.prescription import Prescription

bp = Blueprint('prescriptions', __name__, url_prefix='/prescriptions')

@bp.route('/', methods=['POST'])
def create_prescription():
    medication = request.json['medication']
    dosage = request.json['dosage']
    patient_id = request.json['patient_id']
    priority_score = request.json['priority_score']

    new_prescription = Prescription(medication, dosage, patient_id, priority_score)
    db.session.add(new_prescription)
    db.session.commit()

    return jsonify({'message': 'Prescripción creada con éxito', 'prescription_id': new_prescription.id})
