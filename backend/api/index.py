import os
import sys

# Ensure parent folder (project root for backend) is on the path so we can
# import `main` from the backend root where `main.py` lives.
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app  # expose `app` for Vercel's Python runtime
