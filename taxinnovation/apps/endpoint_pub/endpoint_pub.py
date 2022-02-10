from views import views
from flask import Flask


app = Flask(__name__)

# Agregamos vistas
app.add_url_rule('/', view_func=views.publica_topico, methods=['POST'])
