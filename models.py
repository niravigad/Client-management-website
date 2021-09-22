from . import db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50))
    ip_address = db.Column(db.String(length=20))
    Teudat_Zehut = db.Column(db.String(length=50))
    phone = db.Column(db.String(length=16))
