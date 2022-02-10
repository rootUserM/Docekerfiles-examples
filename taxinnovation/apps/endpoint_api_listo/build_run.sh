#!/bin/bash
export nombre_cont="gcr.io/tax-innovation-produccion/endpoint-api-listo"
export version=":v0.0.2"
docker build --network=host --tag $nombre_cont$version .;
docker push $nombre_cont$version;
docker run -it --entrypoint /bin/bash --network=host -v $PWD:/app 566b3162118e;