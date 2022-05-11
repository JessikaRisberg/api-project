from flask import Blueprint, render_template, redirect, url_for, request, flash
#from flask_login import login_user


# Create a bluprint object that can be used as an app object for this blueprint
bp_open = Blueprint('bp_open', __name__)


@bp_open.get('/')
def index():
    return render_template('index.html')

