from flask import request, current_app


class RequestUtil:
    @staticmethod
    def __dict_pretty(dict):
        ignore_param_list = current_app.config['REQUEST_INFO_LOG_IGNORE_PARAMS'].split(
            ',')
        param_dict = dict.to_dict()
        for param in ignore_param_list:
            if param in param_dict:
                del param_dict[param]
        return ''.join(['[' + key + '=' + value + ']' for key, value in param_dict.items()])

    @staticmethod
    def request_info(request):
        http_method = request.method
        info = current_app.config['APP_NAME']
        info += '[' + http_method + ']' + request.path
        if 'GET' == http_method:
            info += RequestUtil.__dict_pretty(request.args)
        elif 'POST' == http_method:
            info += RequestUtil.__dict_pretty(request.form)
            info += '[post_data=' + request.get_data(as_text=True) + ']'
        return info
