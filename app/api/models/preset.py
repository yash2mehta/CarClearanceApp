from datetime import datetime
from app import db

class Preset(db.Model):
    """Model for storing preset information."""
    __tablename__ = 'preset'
    
    preset_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    preset_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_sensitive_information.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('UserSensitiveInformation', backref='presets')
    travellers = db.relationship('PresetTraveller', backref='preset', cascade='all, delete-orphan')

class PresetTraveller(db.Model):
    """Model for storing preset-traveller relationships."""
    __tablename__ = 'preset_traveller'
    
    preset_traveller_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    preset_id = db.Column(db.Integer, db.ForeignKey('preset.preset_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_sensitive_information.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    traveller = db.relationship('UserSensitiveInformation', backref='preset_travellers') 