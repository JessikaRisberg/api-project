from flask import Blueprint, render_template, redirect, url_for, request, flash


# Create a bluprint object that can be used as an app object for this blueprint
bp_admin = Blueprint('bp_admin', __name__)


@bp_admin.get('/admin')
def index():
    return render_template('admin.html')