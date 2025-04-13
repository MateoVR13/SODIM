from app import db

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medication = db.Column(db.String(255), nullable=False)
    dosage = db.Column(db.String(255), nullable=False)
    patient_id = db.Column(db.Integer, nullable=False)
    priority_score = db.Column(db.Float, nullable=False)

    def __init__(self, medication, dosage, patient_id, priority_score):
        self.medication = medication
        self.dosage = dosage
        self.patient_id = patient_id
        self.priority_score = priority_score
