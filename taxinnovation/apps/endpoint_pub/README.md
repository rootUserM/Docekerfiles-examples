Readme Api Listo
Iniciado por Sergio Perez y continuado por Mauricio Olascoaga 

# set variable de arranque flask

set FLASK_APP=endpoint_pub.py

# set variable de gcp cloud

set GOOGLE_APPLICATION_CREDENTIALS=resources/sa_kubernete.json

# correr app 
python -m flask run

# build docker image
docker build -f Dockerfile . -t gcr.io/tax-innovation-produccion/endpoint-pubsub:0.0.0.1

# push docker image 
docker push gcr.io/tax-innovation-produccion/endpoint-pubsub:0.0.0.1

# deploy image en kubectl
kubectl create deployment endpoint-pubsub --image gcr.io/tax-innovation-produccion/endpoint-pubsub:0.0.0.1

# exponer a puerto en especifico
kubectl expose deployment endpoint-pubsub --type=LoadBalancer --port 8080

# checar deployments arriba
kubectl get deployment

# run docker image
docker run -p 8080:8080 gcr.io/tax-innovation-produccion/endpoint-pubsub:0.0.0.1
