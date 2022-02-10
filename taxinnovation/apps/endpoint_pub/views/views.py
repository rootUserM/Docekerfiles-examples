import json
from datetime import datetime
from flask import request, jsonify
from google.cloud import pubsub
import psycopg2
from utils import log_error, constants


def publica_topico():
    error_mensaje = ""
    # Iniciamos conecciones
    try:
        # Creamos cliente pubsub
        clientPS = pubsub.PublisherClient()
        # Conectamos a base postgres en gcloud
        conn = psycopg2.connect(**constants.DATOS_CONN_PG)
    except Exception as ex:
        error_mensaje = "Error en conección con base de datos"
        log_error.logger(error_mensaje, ex)
        return jsonify(error_mensaje), 500

    # Procesamos mensaje
    try:
        mensaje = request.get_json(force=True)
        headers = dict(request.headers)
        if(
            not ('topic' in mensaje) or
            not ('target' in mensaje) or
            not ('action' in mensaje) or
            not ('payload' in mensaje)
        ):
            return jsonify('Define topic, suscriptor y acción.'), 409

        if not (mensaje['topic'] in constants.ARBOL_MENSAJERIA):
            return jsonify('Topico inexistente'), 409

        if not (mensaje['target'] in constants.ARBOL_MENSAJERIA[mensaje['topic']]):
            return jsonify('Subscriptor inexistente'), 409

        if not (mensaje['action'] in constants.ARBOL_MENSAJERIA[mensaje['topic']][mensaje['target']]):
            return jsonify('Acción inexistente'), 409

        if not isinstance(mensaje['payload'], dict):
            return jsonify('Cuerpo de mensaje invalido, debe ser json'), 409
    except Exception as ex:
        error_mensaje = 'Error en decodificación de mensaje'
        log_error.logger(error_mensaje, ex)
        return jsonify(error_mensaje), 500

    # publicamos mensaje en su topico
    try:
        dir_topico = '{project_id}/topics/{topic}'.format(
            project_id=constants.NOM_PROYECTO,
            topic=mensaje['topic']
        )

        clientPS.publish(
            dir_topico,
            bytes(json.dumps(mensaje), encoding='utf8')
        )
    except Exception as ex:
        error_mensaje = 'Error publicando mensaje en tópico "%s"', mensaje['topic']
        log_error.logger(error_mensaje, ex)
        return jsonify(error_mensaje), 500

    # Guardamos mensaje y metadatos en bitacora
    try:
        with conn.cursor() as curs:
            curs.execute(
                """INSERT INTO messaging_store (
                    topic,
                    target,
                    action,
                    headers,
                    timestamp,
                    payload
                )
                 VALUES (%s,%s,%s, %s, %s, %s)""",
                (
                    mensaje['topic'],
                    mensaje['target'],
                    mensaje['action'],
                    json.dumps(headers),
                    datetime.now().isoformat(),
                    json.dumps(mensaje['payload'])
                )
            )
    except Exception as ex:
        error_mensaje = 'Error guardanto mensaje en bitácora'
        log_error.logger(error_mensaje, ex)
        return jsonify(error_mensaje), 500

    # Matamos Conecciones
    try:
        conn.commit()
        conn.close()
        clientPS.stop()
        del conn
        del clientPS
    except Exception as ex:
        error_mensaje = 'Error cerrando conecciones, el mensaje pudo no ser guardado'
        log_error.logger(error_mensaje, ex)
        return jsonify(error_mensaje), 500
    return jsonify('Mensaje publicado y registrado'), 200
