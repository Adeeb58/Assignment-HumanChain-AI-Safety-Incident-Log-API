import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy  # <--- Importing SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import pytz
from marshmallow import fields, validate, ValidationError, Schema

# --- Basic Flask App Setup ---
app = Flask(__name__)

# --- Configuration (DATABASE is configured here) ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'my_very_secret_key_basic'
# ---vvv DATABASE CONFIG vvv---
# This line tells SQLAlchemy to use a SQLite database file named 'incident_basic.db'
# located in the same directory as this script.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'incident_basic.db')
# ---^^^ DATABASE CONFIG ^^^---
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_SILENCE_UBER_WARNING'] = 1


# --- DATABASE and Marshmallow Initialization ---
# ---vvv DATABASE INIT vvv---
db = SQLAlchemy(app) # <--- Initializing SQLAlchemy with the Flask app
# ---^^^ DATABASE INIT ^^^---
ma = Marshmallow(app)


# ---vvv DATABASE MODEL DEFINITION (SQLAlchemy) vvv---
# This class defines the structure of the 'incidents_basic' table in the database.
class Incident(db.Model):
    __tablename__ = 'incidents_basic'

    id = db.Column(db.Integer, primary_key=True) # Database will auto-generate IDs
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    reported_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(pytz.utc)) # DB/SQLAlchemy handles timestamp

    def __repr__(self):
        return f'<Incident {self.id}: {self.title}>'
# ---^^^ DATABASE MODEL DEFINITION ^^^---


# --- Data Schema Definition (Marshmallow - for JSON handling) ---
ALLOWED_SEVERITIES = ["Low", "Medium", "High"]
class IncidentSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    reported_at = fields.DateTime(dump_only=True, format='iso')
    title = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    severity = fields.Str(required=True, validate=validate.OneOf(ALLOWED_SEVERITIES))
    class Meta:
        ordered = True

incident_schema = IncidentSchema()
incidents_schema = IncidentSchema(many=True)


# --- API Route Definitions (Interacting with DATABASE) ---

@app.route('/incidents', methods=['GET'])
def get_incidents():
    """Retrieve all incidents FROM THE DATABASE""" # <--- Reading from DB
    try:
        # ---vvv DATABASE READ vvv---
        all_incidents = Incident.query.order_by(Incident.reported_at.desc()).all()
        # ---^^^ DATABASE READ ^^^---
        result = incidents_schema.dump(all_incidents)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error getting incidents: {e}")
        return jsonify({"message": "Error retrieving incidents"}), 500

@app.route('/incidents', methods=['POST'])
def add_incident():
    """Log a new incident TO THE DATABASE""" # <--- Writing to DB
    json_data = request.get_json()
    if not json_data: return jsonify({"message": "No input data"}), 400

    try:
        data = incident_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_incident = Incident(
        title=data['title'], description=data['description'], severity=data['severity']
    )

    try:
        # ---vvv DATABASE WRITE vvv---
        db.session.add(new_incident) # Add the new object to the session
        db.session.commit()          # Save changes permanently to the database file
        # ---^^^ DATABASE WRITE ^^^---
        app.logger.info(f"Added new incident with ID {new_incident.id}")
        result = incident_schema.dump(new_incident)
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback() # Undo changes if error occurs
        app.logger.error(f"Error adding incident: {e}")
        return jsonify({"message": "Error saving incident"}), 500


@app.route('/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    """Retrieve a specific incident by ID FROM THE DATABASE""" # <--- Reading from DB
    try:
        # ---vvv DATABASE READ vvv---
        incident = Incident.query.get(incident_id) # Find by primary key
        # ---^^^ DATABASE READ ^^^---
        if incident is None: return jsonify({"message": "Incident not found"}), 404
        result = incident_schema.dump(incident)
        return jsonify(result)
    except Exception as e:
         app.logger.error(f"Error getting incident {incident_id}: {e}")
         return jsonify({"message": "Error retrieving details"}), 500


@app.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    """Delete a specific incident by ID FROM THE DATABASE""" # <--- Deleting from DB
    try:
        # ---vvv DATABASE READ/DELETE vvv---
        incident = Incident.query.get(incident_id) # Find it first
        if incident is None: return jsonify({"message": "Incident not found"}), 404
        db.session.delete(incident) # Mark for deletion
        db.session.commit()         # Make deletion permanent in the database file
        # ---^^^ DATABASE READ/DELETE ^^^---
        app.logger.info(f"Deleted incident {incident_id}")
        return '', 204
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting incident {incident_id}: {e}")
        return jsonify({"message": "Error deleting incident"}), 500


# ---vvv Create DATABASE Tables vvv---
# This ensures the 'incidents_basic' table exists in the 'incident_basic.db' file.
with app.app_context():
    print("Creating database tables if they don't exist...")
    db.create_all() # <--- Creates tables based on the Incident model
    print("Database tables checked/created.")
# ---^^^ Create DATABASE Tables ^^^---


# --- Run the Application ---
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)