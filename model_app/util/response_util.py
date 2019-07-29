from flask import jsonify

from ..base.response_base import ResponseBase


class ResponseUtil:
    @staticmethod
    def success(data):
        return jsonify(ResponseBase('200', '成功', data).__dict__)

    @staticmethod
    def fail():
        return jsonify(ResponseBase('500', '错误').__dict__)
