from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Make, Model, Vehicle
from app import db

vehicle = Blueprint('vehicle', __name__)

@vehicle.route('/vehicle/<id>', methods=['GET', 'POST'])
def vehicle(id):
	vehicle_to_render = Vehicle.query.get(vehicle_id)

	return render_template('vehicles/car_page.html', car=vehicle_to_render)