from flask import Blueprint, request, jsonify
from app.models.non_pos import NonPos

bp = Blueprint('non_pos', __name__, url_prefix='/non_pos')

@bp.route('/', methods=['POST'])
def create_non_pos_order():
    medication_id = request.json['medication_id']
    patient_id = request.json['patient_id']
    authorization_status = 'pending'

    new_non_pos = NonPos(medication_id, patient_id, authorization_status)
    db.session.add(new_non_pos)
    db.session.commit()

    return jsonify({'message': 'Orden No POS creada', 'non_pos_id': new_non_pos.id})
