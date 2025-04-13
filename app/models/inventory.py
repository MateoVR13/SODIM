from app import db

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __init__(self, medication_id, stock):
        self.medication_id = medication_id
        self.stock = stock
