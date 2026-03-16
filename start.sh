#!/bin/sh
pip3 install --no-cache-dir --target ./deps -r ./requirements.txt
PYTHONPATH=./deps python3 -m uvicorn app:app --host 0.0.0.0 --port 8080
