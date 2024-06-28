from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Schema(db.Model):
    __tablename__ = 'schemas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    database = db.Column(db.String(50))
    schema = db.Column(db.String(50))
    freq = db.Column(db.String(50))
    life_time = db.Column(db.String(50), default=31) # value in days


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(50))
    freq = db.Column(db.String(50))


class Backup(db.Model):
    __tablename__ = 'backups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(50))
    created = db.Column(db.String(50))
    life_time = db.Column(db.String(50))
