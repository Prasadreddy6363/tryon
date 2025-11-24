import os
import sys
import subprocess
from pathlib import Path

# Add the web directory to Python path
web_dir = Path(__file__).resolve().parent / 'web'
sys.path.insert(0, str(web_dir))

# Import the app
from app import app, tryon

# Test the tryon function
if __name__ == '__main__':
    with app.test_request_context('/tryon', method='POST', data={'person': '00013_00.jpg', 'cloth': '00006_00.jpg'}):
        try:
            # This will call the tryon function
            result = tryon()
            print("Tryon function executed successfully")
            print(result)
        except Exception as e:
            print(f"Error in tryon function: {e}")
            import traceback
            traceback.print_exc()