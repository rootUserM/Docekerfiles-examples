from views import views
from flask import Flask

DEBUG_NO_ACTIVO = False

app = Flask(__name__)
# Agregamos vistas
app.add_url_rule('/API/ListoMX/ValidaCeic', endpoint='valida_ceic', view_func=views.valida_ceic, methods=['POST'])
app.add_url_rule('/API/ListoMX/TotalCfdis', endpoint='total_cfdis', view_func=views.total_cfdis, methods=['POST'])

app.add_url_rule('/API/tim/DescargaInformacion', endpoint='desc_info', view_func=views.desc_info, methods=['POST'])
app.add_url_rule('/API/ListoMX/RegistrarUsuario', endpoint='registrar_nuevo_cliente', view_func=views.registrar_nuevo_cliente, methods=['POST'])


if(DEBUG_NO_ACTIVO):
    app.run(debug=False)
