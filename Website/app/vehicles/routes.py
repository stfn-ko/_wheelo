from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Vehicle
from app import db

vehicle = Blueprint('vehicle', __name__)
