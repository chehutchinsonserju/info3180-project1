from . import db


class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    property_type = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(255))

    def __repr__(self):
        return '<Property %r>' % self.title
