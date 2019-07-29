from flask import Blueprint, current_app, request, escape
import json

from ..util.response_util import ResponseUtil
from ..model.echo.echo_msg import EchoMsg 

mod = Blueprint('model_echo', __name__)


@mod.route("/echo/<msg>", methods=['GET'])
def echo(msg):
    '''参照http://flask.pocoo.org/docs/1.0/quickstart/#variable-rules'''
    return EchoMsg.go(escape(msg))
