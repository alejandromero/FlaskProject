from app import db

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(30), nullable = False)
    password = db.Column(db.String(80), nullable = False)
    admin = db.Column(db.Boolean, nullable = False, default = False)
    publicimages = db.relationship('PublicImages', backref = 'owner')
    privateimages = db.relationship('PrivateImages', backref = "owner")


class PublicImages(db.Model):
    __tablename__ = "publicimages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(260), unique = True, nullable = False)
    extension = db.Column(db.String(250), unique = True, nullable = False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)


class PrivateImages(db.Model):
    __tablename__ = "privateimages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(260), unique=True, nullable=False)
    extension = db.Column(db.String(250), unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


#The backref option in the relatioship is to provide to the class that is related with and "virtual" atribute that return's the
#object wich is related to; in this case for example PublicImages.owner returns an User object and PublicImages.owner_id only
#return the id of the object