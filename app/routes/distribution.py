from flask import Blueprint, request, jsonify
from app.models.order import Order

bp = Blueprint('distribution', __name__, url_prefix='/distribution')

@bp.route('/order', methods=['POST'])
def process_order():
    prescription_id = request.json['prescription_id']
    status = 'pending'
    delivery_date = '2025-01-01'

    new_order = Order(prescription_id, status, delivery_date)
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Orden de entrega procesada', 'order_id': new_order.id})
