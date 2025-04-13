from flask import Blueprint, request, jsonify
from app.models.inventory import Inventory

bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@bp.route('/check', methods=['GET'])
def check_inventory():
    medication_id = request.args.get('medication_id')
    inventory_item = Inventory.query.filter_by(medication_id=medication_id).first()

    if inventory_item:
        return jsonify({'stock': inventory_item.stock})
    else:
        return jsonify({'message': 'Medicación no disponible'}), 404
