from flask import Flask
from flask_cors import CORS
from routes.api import api_bp
import config
import os

# Create data directories if they don't exist
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(config.CHROMA_DB_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)