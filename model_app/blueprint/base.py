import os

from flask import Blueprint, current_app, send_from_directory

mod = Blueprint('base', __name__)


@mod.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
