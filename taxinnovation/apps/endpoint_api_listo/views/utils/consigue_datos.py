# -*- coding: utf-8 -*-
import asyncio
import aiohttp
#from taxinnovation.apps.endpoint_api_listo.views.utils import constants
from utils import constants
from contextvars import ContextVar
from collections import deque
import copy
import tracemalloc
from concurrent.futures import ThreadPoolExecutor
import janus
import json
import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extensions import AsIs
from io import StringIO
from psycopg2.extensions import register_adapter
import pandas as pd

class download_madre:
    def main(data):
        
        tokensin = str(data['token'])
        rfc_idsin = int(data['rfc_id'])

        res = Scrapper.scrape(
            token=tokensin,
            rfc_id=rfc_idsin
        )

        """with open('resources\\tim.json', 'w', encoding='utf-8') as fil:
            json.dump(query, fil, ensure_ascii=False)

        with open('resources\\tim.json', 'r', encoding='utf-8') as fil:
            res = json.load(fil)"""

        orden_cardinalidad = [
            'rfc',
            'declaraciones_periodo',
            'declaraciones_declaracion',
            'declaraciones_diot',
            'declaraciones_impuesto',
            'declaraciones_balanzacredito',
            'cfdis_factura',
            'cfdis_articulo',
            'cfdis_impuesto',
            'cfdis_documento',
            'cfdis_archivo',
            'cfdis_pago',
            'cfdis_recibo',
            'relacion_factura_pago',
        ]

        register_adapter(dict, psycopg2.extras.Json)
        register_adapter(list, psycopg2.extras.Json)
        conn = psycopg2.connect(**constants.DATOS_CONN_PG)
        conn.set_client_encoding('utf-8')
        curs = conn.cursor()

        for tabla in orden_cardinalidad:
            nom_items = 'api_listomx_{}'.format(tabla)
            df_items_neg = pd.DataFrame.from_records(res[tabla])
            df_items = df_items_neg.where(pd.notnull(df_items_neg), None)
            col_items = ','.join(list(df_items.columns))
            tuples = [copy.deepcopy(tuple(x)) for x in df_items.itertuples(index=False)]
            query = 'INSERT INTO %s(%s) VALUES ' % (nom_items, col_items) + '%s ON CONFLICT DO NOTHING'
            with open('query.json', 'w', encoding='utf-8') as fil:
                json.dump(query, fil, ensure_ascii=False)
            try:
                execute_values(curs, query, tuples)
                conn.commit()
            except Exception as error:
                print('Error: %s' % error)
                conn.rollback()
        print('Datos Guardados [ OK ]')


class Scrapper(object):
    @staticmethod
    async def worker(fila_peticiones, pila_respuestas, token):
        try:
            fila = fila_peticiones.get().async_q
            loop = asyncio.get_event_loop()
            sesion = aiohttp.ClientSession(headers={'Authorization': 'Token ' + token})
            while True:
                item = await fila.get()
                # Separamos llave y variable
                k, v = item.popitem()

                # Switcheamos item de la pila, creamos objeto adecuado
                ob_temp = None
                if k == 'declaraciones_periodo':
                    ob_temp = DeclaracionesPeriodo(
                        fila_peticiones,
                        pila_respuestas,
                        sesion,
                        datos=v
                    )
                elif k == 'declaraciones_declaracion':
                    ob_temp = DeclaracionesDeclaracion(
                        fila_peticiones,
                        pila_respuestas,
                        sesion,
                        datos=v
                    )
                elif k == 'declaraciones_balanzacredito':
                    ob_temp = DeclaracionesBalanzaCred(
                        fila_peticiones,
                        pila_respuestas,
                        sesion,
                        datos=v
                    )
                elif k == 'bancos_transaccion':
                    ob_temp = BancosTransaccion(
                        fila_peticiones,
                        pila_respuestas,
                        sesion,
                        datos=v
                    )
                elif k == 'bancos_reconciliacion':
                    ob_temp = BancosReconciliacion(
                        fila_peticiones,
                        pila_respuestas,
                        sesion,
                        datos=v
                    )
                elif k == 'cfdis_recibo':
                    ob_temp = CFDISRecibo(
                        fila_peticiones,
                        pila_respuestas,
                        sesion,
                        datos=v
                    )
                elif k == 'cfdis_pago':
                    ob_temp = CFDISPago(
                        fila_peticiones,
                        pila_respuestas,
                        sesion,
                        datos=v
                    )
                elif k == 'cfdis_factura':
                    ob_temp = CFDISFactura(
                        fila_peticiones,
                        pila_respuestas,
                        sesion,
                        datos=v
                    )
                elif k == 'cfdis_articulo':
                    ob_temp = CFDISArticulo(
                        fila_peticiones,
                        pila_respuestas,
                        sesion,
                        datos=v
                    )
                elif k == 'cfdis_documento':
                    ob_temp = CFDISDocumento(
                        fila_peticiones,
                        pila_respuestas,
                        sesion,
                        datos=v
                    )
                elif k == 'relacion_factura_pago':
                    ob_temp = RelacionFacturaPago(
                        fila_peticiones,
                        pila_respuestas,
                        sesion,
                        datos=v
                    )

                pila = pila_respuestas[k].get()

                if ob_temp is not None:
                    loop.run_in_executor(
                        None,
                        pila.append,
                        await ob_temp.get_datos()
                    )
                else:
                    print('detalle {} working (ready)'.format(k))
                    loop.run_in_executor(
                        None,
                        pila.append,
                        copy.deepcopy(v)
                    )
                # MArcamos tarea
                loop.call_soon_threadsafe(
                    fila.task_done
                )
        except Exception as ex:
            print(ex)
            await sesion.close()

    @ staticmethod
    async def kickstart(token, rfc_id):
        # Variables para lo asincrono
        loop = asyncio.get_event_loop()
        loop.set_debug(False)
        loop.set_exception_handler(
            lambda loop, context:
                True
        )
        pool = ThreadPoolExecutor(120)
        loop.set_default_executor(pool)
        sesion = aiohttp.ClientSession(headers={'Authorization': 'Token ' + token})

        # Fila multihilos para procesar
        fila_peticiones = ContextVar('fila_peticiones')
        fila_peticiones.set(janus.Queue())

        # Dict de pila multihilos
        mapa_pila_respuestas = {
            'rfc': ContextVar('rfc'),
            'relacion_rfc_clientes': ContextVar('relacion_rfc_clientes'),
            'bancos_cuenta': ContextVar('bancos_cuenta'),
            'bancos_transaccion': ContextVar('bancos_transaccion'),
            'bancos_reconciliacion': ContextVar('bancos_reconciliacion'),
            'declaraciones_periodo': ContextVar('declaraciones_periodo'),
            'declaraciones_declaracion': ContextVar('declaraciones_declaracion'),
            'declaraciones_diot': ContextVar('declaraciones_diot'),
            'declaraciones_impuesto': ContextVar('declaraciones_impuesto'),
            'declaraciones_balanzacredito': ContextVar('declaraciones_balanzacredito'),
            'cfdis_recibo': ContextVar('cfdis_recibo'),
            'cfdis_pago': ContextVar('cfdis_pago'),
            'cfdis_factura': ContextVar('cfdis_factura'),
            'cfdis_documento': ContextVar('cfdis_documento'),
            'cfdis_archivo': ContextVar('cfdis_archivo'),
            'cfdis_articulo': ContextVar('cfdis_articulo'),
            'cfdis_impuesto': ContextVar('cfdis_impuesto'),
            'relacion_factura_pago': ContextVar('relacion_factura_pago')
        }
        # Inicializamos pilas
        for pila_respuestas in mapa_pila_respuestas:
            mapa_pila_respuestas[pila_respuestas].set(deque())

        # consigue todas las facturas del cliente, cada factura tiene: (
        #   lista de recibos,
        #   pagos, documentos,
        #   archivos,
        #   articulos comprados e
        #   impuestos
        # )
        lista_facts = loop.create_task(
            CFDISFacturaLista(
                fila_peticiones,
                sesion,
                datos={'rfc_id': rfc_id}
            ).get_lista()
        )
        # Consigue todas las cuentas bancarias
        lista_cuentas = loop.create_task(
            BancosCuentaLista(
                fila_peticiones,
                sesion,
                datos={'rfc_id': rfc_id}
            ).get_lista()
        )
        # Consigue todas las transacciones bancarias, cada transacciones tiene: (
        #   conciliaciones
        # )
        lista_trans = loop.create_task(
            BancosTransaccionLista(
                fila_peticiones,
                sesion,
                datos={'rfc_id': rfc_id}
            ).get_lista()
        )

        await asyncio.gather(
            lista_facts,
            lista_cuentas,
            lista_trans
        )

        # Consigue detalle de cuenta y estado de declaraciones, cada estado tiene: (
        #   periodos,
        #   diots,
        #   declaracines,
        #   balanzas de credito e
        #   impuestos
        # )

        mapa_pila_respuestas['rfc'].get().append(
            await DetalleRFC(
                fila_peticiones,
                mapa_pila_respuestas,
                sesion,
                datos={'rfc_id': rfc_id}
            ).get_datos()
        )

        await sesion.close()

        asyncio.run_coroutine_threadsafe(
            Scrapper.worker(
                fila_peticiones,
                mapa_pila_respuestas,
                token
            ),
            loop=loop
        )

        for i in range(2):
            asyncio.run_coroutine_threadsafe(
                Scrapper.worker(
                    fila_peticiones,
                    mapa_pila_respuestas,
                    token
                ),
                loop=loop
            )

        esperado = fila_peticiones.get().async_q
        await esperado.join()
        resultado_final = {}
        for item in mapa_pila_respuestas:
            resultado_final[item] = list(mapa_pila_respuestas[item].get())

        return resultado_final

    @ staticmethod
    def scrape(token: str, rfc_id: int):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        retorno = loop.run_until_complete(Scrapper.kickstart(token, rfc_id))
        return retorno


# Clases base
class BaseObjListado:
    def __init__(self, sesion, fila_peticiones, nom_tim, url=None, params={'size': 1000}):
        self.loop = asyncio.get_event_loop()
        self.sesion = sesion
        self.fila_peticiones = fila_peticiones
        self.params = params
        self.nom_tim = nom_tim
        self.url = url
        self.lista = []
        self.lista_actualizada = False

    def set_lista(self, items):
        self.lista = items

    async def get_lista(self):
        await self._consigue_datos()
        return self.lista

    async def _consigue_datos(self):
        # Entramos a ambiente asincrono
        temp_lista = []
        offset_count = 0
        count = -1
        fila = self.fila_peticiones.get().async_q

        while True:
            async with self.sesion.get(
                self.url,
                params={**self.params, 'offset': self.params['size']*offset_count}
            ) as resp:
                try:
                    # Conseguimos página
                    assert resp.status == 200
                    self.loop.call_soon_threadsafe(
                        asyncio.ensure_future,
                        items := await resp.json(encoding='utf-8')
                    )
                    # Vemos cuantos items hay
                    print('lista {} working (pagina {})'.format(self.nom_tim, offset_count))
                    if self.nom_tim == 'cfdis_factura':
                        key_vals = 'results'
                    else:
                        key_vals = 'hits'

                    # Registramos total y offset
                    count = items['count'] if count == -1 else count
                    offset_count += 1

                    # mandamos a pila y extendemos la lista
                    for item in items[key_vals]:
                        copia = {
                            self.nom_tim: {
                                **copy.deepcopy(item),
                                'rfc_id': self.rfc_id
                            }
                        }
                        self.loop.call_soon_threadsafe(
                            asyncio.ensure_future,
                            await fila.put(copia)
                        )
                    temp_lista.extend(items[key_vals])
                    # Si listo, cortamos
                    if(count < offset_count*self.params['size']):
                        break
                except AssertionError as e:
                    print('Error en ' + self.url)
                    raise(e)
                except Exception as e:
                    print(e)
        return temp_lista


class BaseObjCarcaza:
    def __init__(self, fila_peticiones, pila_respuestas, sesion, datos, nom_api, nom_tim, url=None, params=['id']):
        self.loop = asyncio.get_event_loop()
        if url is None:
            self.tiene_endpoint = False
            self.detalle_actualzado = True
        else:
            self.tiene_endpoint = True
            self.detalle_actualzado = False
            self.url = url
        self.nom_tim = nom_tim
        self.nom_api = nom_api
        self.fila_peticiones = fila_peticiones
        self.pila_respuestas = pila_respuestas
        self.sesion = sesion
        self.carcaza = datos
        self.params = params
        # Preparamos objeto que los hijos heredarán
        self.heredables = self._fabrica_args()

        if 'id' in self.heredables:
            self.heredables[self.nom_api] = self.heredables.pop('id')

    async def get_datos(self):
        if self.tiene_endpoint:
            if not self.detalle_actualzado:
                self.loop = asyncio.get_event_loop()
                temp = await self._consigue_datos()
                # Quitamos obj redundantes
                for descartes in self.nom_descartar:
                    if not isinstance(temp.get(descartes, 0), int):
                        temp.pop(descartes, {})
        return temp

    async def _consigue_datos(self):
        # Entramos a ambiente asincrono, declaramos variables
        fila = self.fila_peticiones.get().async_q
        # Entramos a pecición
        async with self.sesion.get(
            self.url.format(**self._fabrica_args())
        ) as resp:
            try:
                # Obtenemos objeto
                assert resp.status == 200
                self.loop.call_soon_threadsafe(
                    asyncio.ensure_future,
                    temp := self._wrapper_resp(await resp.json(encoding='utf-8'))
                )
                print('detalle {} working (on {})'.format(
                    self.nom_tim,
                    self.url.format(**self._fabrica_args())
                ))

                # Mandamos hijos a pila
                for hijo in self.nom_api_hijos:
                    # iteramos cada hijo que este objeto tiene
                    nom_api, nom_tim = hijo.popitem()
                    # Con el nombre de la api
                    if isinstance(temp.get(nom_api, []), int):
                        # si es uno nomás
                        hijo_empujable = [{
                            nom_tim: {
                                'id': temp[nom_api],
                                **self.heredables
                            }
                        }]
                    else:
                        # si son varios
                        hijo_empujable = []
                        for carc_hijo in temp.pop(nom_api, []):
                            hijo_empujable.append({
                                nom_tim: copy.deepcopy(
                                    {**carc_hijo, **self.heredables}
                                )
                            })

                    for item in hijo_empujable:
                        self.loop.call_soon_threadsafe(
                            asyncio.ensure_future,
                            await fila.put(item)
                        )
            except AssertionError:
                print('Error en {}, mandando carcaza a pila...'.format(self.url.format(**self._fabrica_args())))
                temp = self.carcaza
            except Exception as e:
                print(e)
            # Mandamos a pila de resultados
        return temp

    def _wrapper_resp(self, resp):
        return copy.deepcopy(resp)

    def _fabrica_args(self):
        retorno = {}
        for arg in self.params:
            retorno[arg] = self.carcaza[arg]

        return retorno


# Declaraciones
class DetalleRFC(BaseObjCarcaza):
    async def _consigue_datos(self):
        print('Cargando información de perfil... ({})'.format(self.carcaza['rfc_id']))

        async with self.sesion.get(
            'https://listo.mx/api/customers/rfcs/'
        ) as resp:
            assert resp.status == 200
            self.loop.call_soon_threadsafe(
                asyncio.ensure_future,
                temp_cuenta := (await resp.json(encoding='utf-8')).pop()
            )
        async with self.sesion.get(
            self.url.format(**self._fabrica_args())
        ) as resp:
            assert resp.status == 200
            self.loop.call_soon_threadsafe(
                asyncio.ensure_future,
                temp_decl := await resp.json(encoding='utf-8')
            )
        fila = self.fila_peticiones.get().async_q
        for periodo in temp_decl.pop('filing_periods', []):
            copia = copy.deepcopy(periodo)
            self.loop.call_soon_threadsafe(
                asyncio.ensure_future,
                await fila.put({'declaraciones_periodo': copia})
            )
        return {**temp_cuenta, **temp_decl}

    def __init__(self, fila_peticiones, pila_respuestas, sesion, datos={}):
        assert 'rfc_id' in datos
        assert isinstance(datos['rfc_id'], int)
        super().__init__(
            fila_peticiones,
            pila_respuestas['rfc'],
            sesion,
            datos,
            'rfc',
            'rfc',
            'https://listo.mx/api/filings/rfcs/{rfc_id}/status',
            ['rfc_id']
        )
        self.nom_api_hijos = [
            {'electronic_accounting_filings': 'declaraciones_electronicas'},
            {'filing_periods': 'declaraciones_periodo'}
        ]
        self.nom_descartar = ['download_status']


class DeclaracionesPeriodo(BaseObjCarcaza):
    def __init__(self, fila_peticiones, pila_respuestas, sesion, datos={}):
        assert 'id' in datos
        assert isinstance(datos['id'], int)
        super().__init__(
            fila_peticiones,
            pila_respuestas['declaraciones_periodo'],
            sesion,
            datos,
            'filing_period',
            'declaraciones_periodo',
            'https://listo.mx/api/filings/filing_periods/{id}'
        )
        self.nom_api_hijos = [
            {'filings': 'declaraciones_declaracion'},
            {'diots': 'declaraciones_diot'}
        ]
        self.nom_descartar = ['taxes', 'electronic_accounting_filings']


class DeclaracionesDeclaracion(BaseObjCarcaza):
    def __init__(self, fila_peticiones, pila_respuestas, sesion, datos={}):
        assert 'id' in datos
        assert isinstance(datos['id'], int)
        super().__init__(
            fila_peticiones,
            pila_respuestas['declaraciones_declaracion'],
            sesion,
            datos,
            'filing',
            'declaraciones_declaracion',
            'https://listo.mx/api/filings/filings/{id}'
        )
        self.nom_api_hijos = [
            {'credit_balance_reductions': 'declaraciones_balanzacredito'},
            {'credit_balance_originations': 'declaraciones_balanzacredito'},
            {'taxes': 'declaraciones_impuesto'}
        ]
        self.nom_descartar = ['filing_period','financial_statement']


class DeclaracionesBalanzaCred(BaseObjCarcaza):
    def __init__(self, fila_peticiones, pila_respuestas, sesion, datos={}):
        assert 'id' in datos
        assert isinstance(datos['id'], int)
        super().__init__(
            fila_peticiones,
            pila_respuestas['declaraciones_balanzacredito'],
            sesion,
            datos,
            'creditbalance',
            'declaraciones_balanzacredito',
            'https://listo.mx/api/filings/creditbalances/{id}'
        )
        self.nom_api_hijos = []
        self.nom_descartar = ['filing', 'reduction_filing']


class BancosCuentaLista(BaseObjListado):
    async def _consigue_datos(self):
        fila = self.fila_peticiones.get().async_q
        self.loop = asyncio.get_event_loop()

        # Entramos a pecición
        async with self.sesion.get(
            self.url
        ) as resp:
            try:
                # Obtenemos objeto
                assert resp.status == 200
                self.loop.call_soon_threadsafe(
                    asyncio.ensure_future,
                    temp := (await resp.json(encoding='utf-8'))['facets']['bank_account']
                )
                print('detalle {} working (on {})'.format(
                    self.nom_tim,
                    self.url
                ))
                hijo_empujable = []
                for cuenta in temp:
                    hijo_empujable.append({
                        self.nom_tim: {**cuenta, 'rfc_id': self.rfc_id}
                    })

                for item in hijo_empujable:
                    copia = copy.deepcopy(item)
                    self.loop.call_soon_threadsafe(
                        asyncio.ensure_future,
                        await fila.put(copia)
                    )
            except AssertionError:
                print('Error en {}, mandando carcaza a pila...'.format(self.url.format(**self._fabrica_args())))
            except Exception as e:
                print(e.__traceback__)
            # Mandamos a pila de resultados
        return temp

    def __init__(self, fila_peticiones, sesion, datos={}):
        assert 'rfc_id' in datos
        assert isinstance(datos['rfc_id'], int)
        self.rfc_id = datos['rfc_id']
        super().__init__(
            sesion,
            fila_peticiones,
            'bancos_cuenta',
            'https://listo.mx/api/banks/bank_transaction/facets',
            {},
        )


# Cuentas bancarias
class BancosTransaccionLista(BaseObjListado):
    def __init__(self, fila_peticiones, sesion, datos={}):
        assert 'rfc_id' in datos
        assert isinstance(datos['rfc_id'], int)
        self.rfc_id = datos['rfc_id']
        super().__init__(
            sesion,
            fila_peticiones,
            'bancos_transaccion',
            'https://listo.mx/api/banks/bank_transaction',
            {'size': 200},
        )


class BancosTransaccion(BaseObjCarcaza):
    async def get_datos(self):
        fila = self.fila_peticiones.get().async_q
        self.loop = asyncio.get_event_loop()
        for item in self.carcaza.pop('reconciliation_links', []):
            copia = copy.deepcopy({
                'bancos_reconciliacion': {
                    **item,
                    'rfc_id': self.carcaza['rfc_id'],
                    'transaction_id': self.carcaza['value']
                }
            })
            self.loop.call_soon_threadsafe(
                asyncio.ensure_future,
                await fila.put(copia)
            )
        for descartes in self.nom_descartar:
            if not isinstance(self.carcaza.get(descartes, 0), int):
                self.carcaza.pop(descartes, {})
        return self.carcaza

    def __init__(self, fila_peticiones, pila_respuestas, sesion, datos={}):
        assert 'rfc_id' in datos
        assert isinstance(datos['rfc_id'], int)
        super().__init__(
            fila_peticiones,
            pila_respuestas['bancos_transaccion'],
            sesion,
            datos,
            'transaction',
            'bancos_transaccion'
        )


class BancosReconciliacion(BaseObjCarcaza):
    def __init__(self, fila_peticiones, pila_respuestas, sesion, datos={}):
        assert 'rfc_id' in datos
        assert isinstance(datos['rfc_id'], int)
        assert 'transaction_id' in datos
        assert isinstance(datos['transaction_id'], int)
        super().__init__(
            fila_peticiones,
            pila_respuestas['bancos_reconciliacion'],
            sesion,
            datos,
            'reconciliation_link',
            'bancos_reconciliacion',
            'https://listo.mx/api/banks/{rfc_id}/transactions/{transaction_id}/reconciliation/info',
            ['rfc_id', 'transaction_id']
        )
        self.nom_api_hijos = []
        self.nom_descartar = []


# Facturas
class CFDISFacturaLista(BaseObjListado):
    def __init__(self, fila_peticiones, sesion, datos={}):
        assert 'rfc_id' in datos
        assert isinstance(datos['rfc_id'], int)
        self.rfc_id = datos['rfc_id']
        super().__init__(
            sesion,
            fila_peticiones,
            'cfdis_factura',
            'https://listo.mx/api/invoices/export_json',
            params={'size': 1000}
            # params={'size': 1, 'ids': 304640111}
        )


class CFDISFactura(BaseObjCarcaza):
    def __init__(self, fila_peticiones, pila_respuestas, sesion, datos={}):
        assert 'id' in datos
        assert isinstance(datos['id'], int)
        super().__init__(
            fila_peticiones,
            pila_respuestas['cfdis_factura'],
            sesion,
            datos,
            'invoice',
            'cfdis_factura',
            'https://listo.mx/api/invoices/{id}'
        )
        self.nom_api_hijos = [
            {'lineitems': 'cfdis_articulo'},
            {'documents': 'cfdis_documento'},
            {'payment_receipt_entries': 'relacion_factura_pago'}
        ]
        self.nom_descartar = [
            'taxes',
            'item_links',
            'relationships_from',
            'relationships_to',
            'payments',
            'receiver_address',
            'validation_status',
            'validation_status_short',
            'lineitems',
            'pdf_file_ids',
            'xml_file_ids',
            'reimbursable_to',
            'goods_receipts',
            'purchase_orders',
            'email_status',
            'extra_header_fields',
            'log_entries',
            'warnings',
            'total_pass_through_taxes_by_type_mxn',
            'total_retained_taxes_by_type_mxn',
        ]


class CFDISArticulo(BaseObjCarcaza):
    async def get_datos(self):
        self.loop = asyncio.get_event_loop()
        fila = self.fila_peticiones.get().async_q
        print('detalle cfdis_articulo working (ready)')
        for item in self.carcaza.pop('taxes', []):
            copia = copy.deepcopy({
                'cfdis_impuesto': {**item, 'lineitem': self.carcaza['id']}
            })
            self.loop.call_soon_threadsafe(
                asyncio.ensure_future,
                await fila.put(copia)
            )

        for descartes in self.nom_descartar:
            if not isinstance(self.carcaza.get(descartes, 0), int):
                self.carcaza.pop(descartes, {})
        return self.carcaza

    def __init__(self, fila_peticiones, pila_respuestas, sesion, datos={}):
        super().__init__(
            fila_peticiones,
            pila_respuestas['cfdis_articulo'],
            sesion,
            datos,
            'lineitem',
            'cfdis_articulo',
        )
        self.nom_descartar = ['customs']


class CFDISDocumento(BaseObjCarcaza):
    async def get_datos(self):
        self.loop = asyncio.get_event_loop()
        fila = self.fila_peticiones.get().async_q
        print('detalle cfdis_documento working (ready)')
        for item in self.carcaza.pop('files', []):
            del item['documentId']
            copia = copy.deepcopy({
                'cfdis_archivo': {**item, 'document': self.carcaza['id']}
            })
            self.loop.call_soon_threadsafe(
                asyncio.ensure_future,
                await fila.put(copia)
            )
        for descartes in self.nom_descartar:
            if not isinstance(self.carcaza.get(descartes, 0), int):
                self.carcaza.pop(descartes, {})
        return self.carcaza

    def __init__(self, fila_peticiones, pila_respuestas, sesion, datos={}):
        super().__init__(
            fila_peticiones,
            pila_respuestas['cfdis_documento'],
            sesion,
            datos,
            'document',
            'cfdis_documento'
        )
        self.nom_descartar = ['customs']


class CFDISPago(BaseObjCarcaza):
    def __init__(self, fila_peticiones, pila_respuestas, sesion, datos={}):
        assert 'id' in datos
        assert isinstance(datos['id'], int)
        super().__init__(
            fila_peticiones,
            pila_respuestas,
            sesion,
            datos,
            'payment',
            'cfdis_pago',
            'https://listo.mx/api/cfdi_payments/payments/{id}'
        )
        self.nom_api_hijos = [{'receipt_id': 'cfdis_recibo'}]
        self.nom_descartar = ['invoices', 'files','data_warnings']


class CFDISRecibo(BaseObjCarcaza):
    def __init__(self, fila_peticiones, pila_respuestas, sesion, datos={}):
        assert 'id' in datos
        assert isinstance(datos['id'], int)
        super().__init__(
            fila_peticiones,
            pila_respuestas['cfdis_recibo'],
            sesion,
            datos,
            'receipt',
            'cfdis_recibo',
            'https://listo.mx/api/cfdi_payments/receipts/{id}'
        )
        self.nom_api_hijos = []
        self.nom_descartar = ['payments','validation_status','warnings','email_status', 'files']


class RelacionFacturaPago(BaseObjCarcaza):
    async def get_datos(self):
        self.loop = asyncio.get_event_loop()
        fila = self.fila_peticiones.get().async_q

        id_factura = self.carcaza.pop('invoice')
        id_pago = self.carcaza.pop('cfdi_payment_id')
        print('detalle relacion_factura_pago working (ready)')
        copia = {'cfdis_pago': {'id': id_pago}}
        self.loop.call_soon_threadsafe(
            asyncio.ensure_future,
            await fila.put(copia)
        )
        self.carcaza = {'invoice': id_factura, 'payment': id_pago}
        return self.carcaza

    def __init__(self, fila_peticiones, pila_respuestas, sesion, datos={}):
        super().__init__(
            fila_peticiones,
            pila_respuestas['relacion_factura_pago'],
            sesion,
            datos,
            '',
            'relacion_factura_pago',
            params=[]
        )


if __name__ == '__main__':
    main()
