# Import libreries
import sys
import os

# Add the application directory to the Python path
sys.path.insert(0, '/var/www/Control-aulas-sistemas')

# Add the site-packages directory of the virtual environment to the Python path
venv_path = '/var/www/Control-aulas-sistemas/venv/lib/python3.12/site-packages'
sys.path.insert(1, venv_path)

# Import the Flask application
from app import app as application
