from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class UserModel(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)

    records = db.relationship("RecordModel", back_populates="user")

class RecordModel(db.Model):
    __tablename__ = "records"

    record_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(20), nullable=True)
    duration = db.Column(db.String(10), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    description = db.Column(db.String(50),nullable=True)

    user = db.relationship("UserModel",back_populates="records",lazy=True)

    def to_json(self):
        return {
                'record_id': self.record_id,
                'date': self.date,
                'start_time': self.start_time,
                'duration': self.duration,
                'user_id': self.user_id,
                'description' : self.description
                }