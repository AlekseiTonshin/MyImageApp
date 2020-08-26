from gino.ext.sanic import Gino

db = Gino()


class User(db.Model):
    __tablename__ = 'images_test'
    id = db.Column(db.Integer(), primary_key=True)
    picture_old = db.Column(db.LargeBinary())
    picture_new = db.Column(db.LargeBinary())
