# Add this to your Google Colab notebook

# Install required packages if not already installed
!pip install flask flask-cors pyngrok

# Import necessary libraries
import os
from pyngrok import ngrok
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up ngrok authentication - you'll need to sign up for a free ngrok account
# Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
# Replace with your token or set it in your .env file
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN", "your_ngrok_token_here")
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# Start ngrok tunnel to expose the Flask app (assuming Flask runs on port 5000)
public_url = ngrok.connect(5000).public_url
print(f"🚀 Backend is publicly accessible at: {public_url}")
print(f"⚠️ Update your frontend API_URL to this URL")

# Now run your Flask app
# Make sure your Flask app binds to 0.0.0.0
!cd backend && python app.py
