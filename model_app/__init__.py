import traceback

from flask import Flask, request

from config.log import LogConfigLoader
from .util.request_util import RequestUtil
from .util.response_util import ResponseUtil


def create_app(instance_config_filename):
    """create_app设计参照: http://flask.pocoo.org/docs/1.0/patterns/appfactories/"""

    app = Flask(__name__, instance_relative_config=True)

    app_config(app, instance_config_filename)
    app_log(app)
    app_aop(app)

    from .blueprint import base
    from .blueprint import health
    from .blueprint import model_echo

    app.register_blueprint(base.mod, url_prefix='/')
    app.register_blueprint(health.mod, url_prefix='/health')
    app.register_blueprint(model_echo.mod, url_prefix='/model')

    return app


def app_config(app, instance_config_filename):
    """不要更改配置文件加载的顺序"""
    app.config.from_object('config.default')
    app.config.from_envvar('APP_CONFIG_FILE')
    app.config.from_pyfile(instance_config_filename)

    '''返回JSON支持中文'''
    app.config['JSON_AS_ASCII'] = False


def app_log(app):
    """加载日志配置"""
    LogConfigLoader.close_werkzeug_logger()
    LogConfigLoader.load_flask_app_logger_config(app.name,
                                                 app.config['LOG_FILE'], app.config['LOG_BACKUP_COUNT'])


def app_aop(app):
    @app.errorhandler(Exception)
    def global_exception_handler(error):
        app.logger.error(traceback.format_exc())
        return ResponseUtil.fail()

    @app.before_request
    def print_request_info():
        app.logger.info(RequestUtil.request_info(request))
