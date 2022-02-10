import os
import json


NOM_PROYECTO = ""
ARBOL_MENSAJERIA = {}
DATOS_CONN_PG = {}

# Obtenemos el nombre del proyecto de la cuenta de servicio
with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS']) as llave:
    NOM_PROYECTO = "projects/" + json.load(llave)['project_id']
# Cargamos el arbol de mensajería (Topic, Target y Action)
with open('resources/arbol_mensajeria.json') as arch:
    ARBOL_MENSAJERIA = json.load(arch)
# Cargamos los datos para conectar a cloudsql
with open('resources/datos_tabla_sql.json') as arch:
    DATOS_CONN_PG = json.load(arch)
