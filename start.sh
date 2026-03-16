#!/bin/sh
pip3 install --no-cache-dir --target /app/deps -r /app/requirements.txt
PYTHONPATH=/app/deps python3 -m uvicorn app:app --host 0.0.0.0 --port 8080
