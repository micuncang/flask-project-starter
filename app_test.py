import os

os.environ['APP_CONFIG_FILE'] = os.path.abspath('config/env/development.py')

from model_app import create_app 

app = create_app('config.py')

app.run(host='0.0.0.0', port=5000)