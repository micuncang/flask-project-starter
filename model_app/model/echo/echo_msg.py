import pkg_resources


class EchoMsg:
    @staticmethod
    def go(msg):
        return EchoMsg.__data.format(msg)


def __load_data():
    with open(pkg_resources.resource_filename(__name__, 'data.txt'), 'r') as f:
        return f.readline()


'''模型在启动时加载初始化文件一次是一种常见的场景，可参照该实现方式'''
EchoMsg._EchoMsg__data = __load_data()
