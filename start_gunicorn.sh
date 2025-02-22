#!/bin/bash
cd /home/pedro/FomoSapiensCryptoDipHunter
source venv/bin/activate
gunicorn --workers 3 --bind 0.0.0.0:8002 fomo_sapiens.wsgi:application
