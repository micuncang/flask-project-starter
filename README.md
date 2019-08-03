## Flask项目快速启动工具

#### 基础知识
* Flask官方网站工程结构参照 [flask-website](https://github.com/pallets/flask-website)
* Python虚拟环境：python3 venv/pyenv+virtualenv/conda
* Instance Fold概念 [[1](http://flask.pocoo.org/docs/1.0/config/#instance-folders)][[2](http://exploreflask.com/en/latest/configuration.html#using-instance-folders)]
* Flask配置注意事项，参照源码[flask/config.py]注释：only <strong>uppercase</strong> keys are added to the config.  This makes it possible to use lowercase values in the config file for temporary values that are not added to the config or to define the config keys in the same file that implements the application.
* 相对导入 vs. 绝对导入 [[1](http://exploreflask.com/en/latest/conventions.html#relative-imports)][[2](http://kuanghy.github.io/2016/07/21/python-import-relative-and-absolute)]
* logging日志模块以及多进程日志风险 [[1](http://doudou0o.com/archives/fe118cd8/python-logging%E6%97%A5%E5%BF%97%E6%A8%A1%E5%9D%97%E4%BB%A5%E5%8F%8A%E5%A4%9A%E8%BF%9B%E7%A8%8B%E6%97%A5%E5%BF%97.html)][[2](https://blog.csdn.net/qq_20690231/article/details/84644939)]
* Blueprint相关概念 [[1](https://www.jianshu.com/p/95d98df72c91)][[2](http://exploreflask.com/en/latest/blueprints.html)]
* Flask上下文和current_app/g相关概念 [[1](http://flask.pocoo.org/docs/1.0/appcontext/)][[2](http://flask.pocoo.org/docs/1.0/reqcontext/)][[3](https://segmentfault.com/a/1190000017814222)][[4](https://blog.csdn.net/Lyj20170608/article/details/79636583)][[5](https://blog.tonyseek.com/post/the-context-mechanism-of-flask/#id11)][[6](https://stackoverflow.com/questions/40881750/whats-the-difference-between-current-app-and-g-context-variable?rq=1)]
* Flask扩展列表 [Flask Extensions](http://flask.pocoo.org/extensions/)
* 部署：While lightweight and easy to use, Flask’s built-in server is not suitable for production as it doesn’t scale well. Some of the options available for properly running Flask in production are documented here. [[1](http://flask.pocoo.org/docs/1.0/deploying/)]

#### 快速开始(py37)

> 虚拟环境可以按需进行调整，此处采用Python3的venv模块

* git clone git@github.com:micuncang/flask-project-starter.git <strong>YOURAPPNAME</strong>
* cd <strong>YOURAPPNAME</strong> && mkdir instance && cd instance && touch config.py && cd ..
* git remote remove origin
* python3 -m venv venv && source venv/bin/activate
* pip install -r requirements.txt
* sh start.sh
* curl http://localhost:5000/health/ping
* sh stop.sh

#### 如何在离线环境使用

在网络受限环境部署系统需要无网从零开始创建纯粹的环境，简称离线环境。本工程倾向于把离线环境安装划分为两部分：Python主体版本安装和Python Module安装，这样喜欢使用pip的同学可以借助conda + pip组合分别进行虚拟环境和模块的维护。其中Python的主体版本不仅包括特定版本的Python安装包，还将包括pip/openssl/wheel/setuptools/sqlite/certifi/libstdcxx等附加程序。！！！安装Python Module前请注意虚拟环境的切换。以下方法都需要先确认好工程希望使用的Python主体版本，然后借助有网环境内先行进行环境准备，最后传输相应资源进入离线环境安装。

##### Python主体版本

> miniconda系列

* miniconda下载地址：[点击进入](https://docs.conda.io/en/latest/miniconda.html)，请注意选择合适的版本
* miniconda脚本可以离线安装，如果想静默执行脚本可添加 '-b' 参数
* 有网环境中建议为每个Python主版本预留纯净环境\<base-version\>，conda create -n \<base-version\> python=\<base-version\>创建虚拟环境。后续可以借助克隆\<base-version\>初始化虚拟环境，conda create -n \<env-name\> --clone \<base-version\>
* 离线环境中conda系列建议借助 '--offline' 初始化空环境，conda create -n \<env-name\> --offline，不需要预置Python主体版本

> anaconda3系列

* anaconda3下载地址：[点击进入](https://www.anaconda.com/distribution/)
* 除下载地址不同外，其他同miniconda

> pyenv/virtualvenv/venv系列

* pyenv本身只进行Python主版本管理，需要借助外部模块来实现虚拟环境管理。virtualvenv以及Python3.3以上版本支持的venv模块可用作虚拟环境维护，该系列方法可作为利基玩家试验使用，暂不推荐在线上环境使用

##### Python Module

> conda系列

* 在有网纯净环境下安装依赖，注意conda需要自己特定的安装包，安装包可从国内镜像下载对应版本，镜像推荐：[清华镜像](https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/)。如果使用conda install可以添加 '-c' 参数指定国内镜像(-c https://mirrors.ustc.edu.cn/anaconda/pkgs/main/)
* 需要理解如下两种导出方式的区别：conda env export -n \<env-name\> > environment.yml 和 conda list -n \<env-name\> -e > requirements.txt，注意这两种方式都会包含python主体版本的信息
* 借助conda list -n \<env-name\> -e | grep -Ev '\^#' > requirements-conda.txt生成工程所需模块依赖
* conda安装目录下pkgs文件夹中会包含所有离线安装包，可以汇总拷贝至离线环境。使用awk -F'=' '{print $1"-"$2"-"$3".tar.bz2"}' requirements-conda.txt可以罗列出所有的模块依赖包，借助罗列的结果可以从pkgs中cp相应包然后离线传输至无网机器中。conda系列的离线安装要略复杂于pip
* 如果安装包过多，可采用脚本方式(for each)借助conda install -n \<env-name\> --use-local安装
* 如果已安装conda-build，可以尝试local-channel，[点击查看具体教程](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/create-custom-channels.html)。建议添加 '--override-channels' 参数
* conda仓库维护的模块种类要少于pip，如果想统一模块维护方式，建议统一使用pip

> pip系列

* 在有网纯净环境下安装相应依赖
* 借助pip freeze > requirements.txt生成工程所需模块依赖
* 借助pip download下载所需模块文件，pip download -d pkgs/ -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ ，其中借助了清华的镜像
* 拷贝pkgs/下模块文件离线传输至无网机器中，使用pip install安装相应模块，pip install --no-index -f file:///\<file-path\>/pkgs/ -r requirements.txt。除非有足够的把握，应当谨慎使用 '--ignore-installed' 参数
