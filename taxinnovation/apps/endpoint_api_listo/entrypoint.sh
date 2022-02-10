#!/bin/bash
# Damos ubicación de llave pubsubn en variable de sistema
export GOOGLE_APPLICATION_CREDENTIALS=resources/keys/sa_kubernete.json
exec gunicorn --config gunicorn_config.py endpoint_api_listo:app