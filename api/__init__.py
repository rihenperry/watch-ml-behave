# Import flask and template operators
from flask import Flask, jsonify
from flask import Blueprint

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# define api blueprint
endpoint = Blueprint('endpoint', __name__)

# Configurations
app.config.from_object('api.config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# import controller
from . import controllers

# register blueprint
app.register_blueprint(endpoint, url_prefix="/api")


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
        return jsonify(error=404, text=str(error)), 404


@app.errorhandler(405)
def method_not_allowed(error):
        return jsonify(error=405, text=str(error)), 405


# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
