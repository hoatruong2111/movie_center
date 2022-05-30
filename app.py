import os
from flask import Flask
from flask_cors import CORS, cross_origin
from blueprints import routes
from models import setup_db
from dotenv import load_dotenv

load_dotenv()

PERMISSON = {
    'CAN_GET_REVIEWS': os.getenv('CAN_GET_REVIEWS'),
    'CAN_POST_MOVIES': os.getenv('CAN_POST_MOVIES'),
    'CAN_POST_REVIEWS': os.getenv('CAN_POST_REVIEWS'),
    'CAN_PATCH_MOVIES': os.getenv('CAN_PATCH_MOVIES'),
    'CAN_DELETE_MOVIES': os.getenv('CAN_DELETE_MOVIES'),
    'CAN_DELETE_REVIEWS': os.getenv('CAN_DELETE_REVIEWS'),
}

app = Flask(__name__)
setup_db(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PATCH,POST,DELETE,OPTIONS')
    return response


app.register_blueprint(routes)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
