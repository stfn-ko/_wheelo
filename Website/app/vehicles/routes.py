from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Make, Model, Vehicle
from app import db

vehicles = Blueprint('vehicle', __name__)

@vehicles.route('/vehicle/<id>', methods=['GET', 'POST'])
def vehicle(id):
	vehicle_to_render = Vehicles.query.get(id)
	makes_for_render = Make.query.order_by(Make.make_id.asc())
    models_for_render = Model.query.order_by(Model.model_id.asc())
	return render_template('vehicles/car_page.html', car=vehicle_to_render, makes=makes_for_render, models=models_for_render)