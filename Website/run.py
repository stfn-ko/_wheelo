from app import create_app
from flask_sqlalchemy import SQLAlchemy

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)