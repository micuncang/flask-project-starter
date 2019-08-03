from datetime import datetime
from multiprocessing import Pool

from flask import Blueprint, current_app, request

from config.log import LogConfigLoader
from ..util.response_util import ResponseUtil

mod = Blueprint('health', __name__)


@mod.route("/ping", methods=['GET'])
def ping():
    msg = '{} @ {}'.format(current_app.config['APP_NAME'], datetime.now().strftime(
        current_app.config['DATETIME_FORMAT']))
    return ResponseUtil.success(msg)


@mod.route("/echo", methods=['POST'])
def echo():
    return ResponseUtil.success(request.form['value'])


@mod.route("/echo_data", methods=['POST'])
def echo_data():
    request_data = request.get_data(as_text=True)
    return ResponseUtil.success(request_data)


@mod.route("/echo_form", methods=['POST'])
def echo_form():
    """
    curl -XPOST -H 'enctype=multipart/form-data' http://localhost:5000/health/echo_form -F 'testfile=@/yourfilepath'
    """
    json_file = request.files['testfile']
    try:
        result = bytes.decode(json_file.read())
    finally:
        json_file.close()
    return ResponseUtil.success(result)


@mod.route("/where", methods=['GET'])
def where():
    return ResponseUtil.success(current_app.config['WHERE'])


@mod.route("/exception", methods=['GET'])
def exception():
    return 1 / 0


def multi_log_task(logger):
    try:
        logger.info('multiprocess logger test')
    except Exception as e:
        current_app.logger.error(e)


@mod.route("/multilog", methods=['GET'])
def multiprocess_log():
    multi_process_logger = LogConfigLoader.multiprocess_log_test_logger()
    pool = Pool(processes=2)
    try:
        for index in range(20000):
            pool.apply_async(multi_log_task, args=(multi_process_logger,))
    finally:
        pool.close()
        pool.join()

    return ResponseUtil.success('multilog test finished')
