from app import db

class NonPos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, nullable=False)
    authorization_status = db.Column(db.String(50), nullable=False)

    def __init__(self, medication_id, patient_id, authorization_status):
        self.medication_id = medication_id
        self.patient_id = patient_id
        self.authorization_status = authorization_status
