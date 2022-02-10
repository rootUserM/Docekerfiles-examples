Readme Api Listo
Iniciado por Sergio Perez y continuado por Mauricio Olascoaga 

# set variable de arranque flask

set FLASK_APP=endpoint_api_listo.py

# set variable de gcp cloud

set GOOGLE_APPLICATION_CREDENTIALS=resources/keys/sa_kubernete.json

# correr app 
python -m flask run


# build docker image
docker build -f Dockerfile . -t gcr.io/tax-innovation-produccion/endpoint-api-listo:0.0.1.0

# push docker image 
docker push gcr.io/tax-innovation-produccion/endpoint-api-listo:0.0.1.0

# deploy image en kubectl
kubectl create deployment endpoint-api-listo --image gcr.io/tax-innovation-produccion/endpoint-api-listo:0.0.1.0

# exponer a puerto en especifico
kubectl expose deployment endpoint-api-listo --type=LoadBalancer --port 8000

# checar deployments arriba
kubectl get deployment

# run docker image
docker run -p 8000:8000 gcr.io/tax-innovation-produccion/endpoint-api-listo:0.0.0.11
