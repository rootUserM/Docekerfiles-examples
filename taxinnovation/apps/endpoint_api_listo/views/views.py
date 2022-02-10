from flask import jsonify, request
from utils import log_error, constants

import aiohttp
import requests


#from taxinnovation.apps.endpoint_api_listo.views.utils.consigue_datos import download_madre
from views.utils.consigue_datos import download_madre

# Conectamos a base postgres en gcloud
def valida_ceic():
    data = request.get_json()
    if data is None:
        return jsonify({'TIM': 'no proveyó json'}), 400
    if 'rfc' not in data or 'ciec' not in data:
        return jsonify({'TIM': 'rfc o ciec faltante'}), 409

    try:
        req = requests.post(
            'https://listo.mx/api/signup/verify_ciec',
            json=data,
            headers={'Authorization': constants.LLAVE_MAESTRA['llave']}
        )

        _, resp = req.json().popitem()

        return jsonify(
            {'LISTO': '{}'.format(resp)}
        ), req.status_code
    except Exception as ex:
        log_error(ex)
        return 'Error interno', 500


async def _valida_ceic(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(
        ) as pet:
            codigo = pet.status
    return codigo


def consulta_inicial(rfc_id=293239030, token_cliente="49b2d85a24a14bf97b9522fe16e98752b7f255f9"):
    results = {}
    hilos = {}

    results['declaraciones'] = hilos['declaraciones'].get()
    results['facturas'] = hilos['facturas'].get()
    results['cuentas'] = hilos['cuentas'].get()
    results['impuestos'] = hilos['impuestos'].get()
    return jsonify(results)


def desc_info():
    data = request.get_json()
    if data is None:
        return jsonify({'TIM': 'no proveyo json'}), 400
    if 'token' not in data or 'rfc_id' not in data:
        return jsonify({'TIM': 'rfc_id o token faltante'}), 409

    download_madre.main(data)

    return jsonify(
        {'Entro': 'Al enpoint desc_info'}
    ), 200


def total_cfdis():
    data = request.get_json()

    try:
        req = requests.get(
            'https://listo.mx/api/invoices/sat_sync_metadata/'+data['rfc_id'],
            json=data,
            headers={'Authorization': 'Token '+data['token']}
        )

        
        resp = req.json()

        return jsonify(
            {'LISTO': '{}'.format(resp)}
        ), req.status_code
    except Exception as ex:
        log_error(ex)
        return 'Error interno', 500


def registrar_nuevo_cliente():
    data = request.get_json()

    if data is None:
        return jsonify({'TIM': 'no proveyó json'}), 400
    if 'rfc' not in data or 'ciec' not in data:
        return jsonify({'TIM': 'rfc o ciec faltante'}), 409

    try:
        req = requests.post(
            'https://listo.mx/api/signup/external',
            json=data,
            headers={'Authorization': constants.LLAVE_MAESTRA['llave']}
        )


        resp = req.json()

        return jsonify(
            {'LISTO': '{}'.format(resp)}
        ), req.status_code
    except Exception as ex:
        log_error(ex)
        return 'Error interno', 500


def consultar_rfc_id():
    data = request.get_json()

    if data is None:
        return jsonify({'TIM': 'no proveyó json'}), 400
    if 'token' not in data:
        return jsonify({'TIM': 'token faltante'}), 409

    try:
        req = requests.post(
            'https://listo.mx/api/signup/external',
            headers={'Authorization': data['token']}
        )

        _, resp = req.json().popitem()

        return jsonify(
            {'LISTO': '{}'.format(resp)}
        ), req.status_code
    except Exception as ex:
        log_error(ex)
        return 'Error interno', 500
