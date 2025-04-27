import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import pytz
from marshmallow import fields, validate, ValidationError, Schema

# --- App, DB, Marshmallow Setup ---
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'my_very_secret_key_basic'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'incident_basic.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_SILENCE_UBER_WARNING'] = 1
db = SQLAlchemy(app)
ma = Marshmallow(app)

# --- Database Model ---
class Incident(db.Model):
    __tablename__ = 'incidents_basic'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    reported_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(pytz.utc))
    # Removed __repr__ for brevity

# --- Schema for Validation/Serialization ---
ALLOWED_SEVERITIES = ["Low", "Medium", "High"]
class IncidentSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    reported_at = fields.DateTime(dump_only=True, format='iso')
    title = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    severity = fields.Str(required=True, validate=validate.OneOf(ALLOWED_SEVERITIES))
    # Removed Meta class for brevity

incident_schema = IncidentSchema()
incidents_schema = IncidentSchema(many=True)

# --- API Routes ---
@app.route('/incidents', methods=['GET'])
def get_incidents():
    try:
        all_incidents = Incident.query.order_by(Incident.reported_at.desc()).all()
        return jsonify(incidents_schema.dump(all_incidents)) # Combined serialization and return
    except Exception as e:
        # Removed logging for brevity
        return jsonify({"message": "Error retrieving incidents"}), 500

@app.route('/incidents', methods=['POST'])
def add_incident():
    json_data = request.get_json()
    if not json_data: return jsonify({"message": "No input data"}), 400
    try:
        data = incident_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_incident = Incident(title=data['title'], description=data['description'], severity=data['severity'])
    try:
        db.session.add(new_incident)
        db.session.commit()
        return jsonify(incident_schema.dump(new_incident)), 201 # Combined serialization and return
    except Exception as e:
        db.session.rollback()
        # Removed logging for brevity
        return jsonify({"message": "Error saving incident"}), 500

@app.route('/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    try:
        incident = Incident.query.get(incident_id)
        if incident is None: return jsonify({"message": "Incident not found"}), 404
        return jsonify(incident_schema.dump(incident)) # Combined serialization and return
    except Exception as e:
        # Removed logging for brevity
         return jsonify({"message": "Error retrieving details"}), 500

@app.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    try:
        incident = Incident.query.get(incident_id)
        if incident is None: return jsonify({"message": "Incident not found"}), 404
        db.session.delete(incident)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        # Removed logging for brevity
        return jsonify({"message": "Error deleting incident"}), 500

# --- Create Database Tables ---
with app.app_context():
    db.create_all() # Removed print statements

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)