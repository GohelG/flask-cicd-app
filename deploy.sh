#!/bin/bash

echo "Deploying Flask Application..."

pkill gunicorn || true

nohup gunicorn app:app -b 0.0.0.0:5000 &