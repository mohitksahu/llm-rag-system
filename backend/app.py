from flask import Flask
from flask_cors import CORS
import config
from routes.api import api_bp
from utils.env_utils import load_environment

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load environment variables (including Hugging Face token)
load_environment()

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    print(f"Starting server on {config.HOST}:{config.PORT}")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)