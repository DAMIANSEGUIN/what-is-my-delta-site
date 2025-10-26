#!/usr/bin/env python3
print("Python is working!")
import sys
print(f"Python version: {sys.version}")
try:
    import fastapi
    print(f"FastAPI version: {fastapi.__version__}")
except ImportError as e:
    print(f"FastAPI import error: {e}")
try:
    import uvicorn
    print(f"Uvicorn version: {uvicorn.__version__}")
except ImportError as e:
    print(f"Uvicorn import error: {e}")