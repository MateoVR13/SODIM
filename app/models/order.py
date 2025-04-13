from app import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescription.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    delivery_date = db.Column(db.String(50), nullable=False)

    def __init__(self, prescription_id, status, delivery_date):
        self.prescription_id = prescription_id
        self.status = status
        self.delivery_date = delivery_date
