"""User auth views."""
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt import settings as jwt_settings
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.template.loader import render_to_string

from taxinnovation.apps.users.permissions.users import isCompanyAdmin
from taxinnovation.apps.users.serializers.auth import (
    UserLoginTokenPairSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer,
    UserInvitationSerializer,
    ChangePasswordSerializer,
    SendEmailChangePasswordSerializer,
    PasswordRecoveryEmail,
    PasswordRecovery
)
from taxinnovation.apps.users.serializers.users import UserModelSerializer
from taxinnovation.apps.users.models import UserProfile, User

import requests

from .firmamex import FirmamexServices

import http.client
import mimetypes
import random
import base64
import json
import datetime
import jwt
from rest_framework_simplejwt import settings as jwt_settings
from django.conf import settings
from .firmamex import FirmamexServices


class UserAuthViewSet(viewsets.GenericViewSet):
    """User authentication API view."""

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['invitation']:
            permissions = [IsAuthenticated, ]
        else:
            permissions = []
        return (permission() for permission in permissions)

    @action(detail=False, methods=['post'])
    def token(self, request, *args, **kwargs):
        serializer = UserLoginTokenPairSerializer(data=request.data, context={'request': request})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='token/refresh')
    def token_refresh(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            data = {
                'detail': e.args[0],
                'code': 'token_expired'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def signup(self, request, *args, **kwargs):
        """Handle HTTP POST request for signup."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request, *args, **kwargs):
        """User account verification API view."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Felicidades, ahora puedes iniciar sesión'
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def tokenVerify(self, request, *args, **kwargs):
        """User account verification API view."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Felicidades, ahora puedes iniciar sesión'
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def invitation(self, request, *args, **kwargs):

        data = {
            'email': request.data['email'],
            'username': request.data['username'],
            'name': request.data['name'],
            'last_name': request.data['last_name'],
            'second_last_name': request.data['second_last_name'],
            'phone_number': request.data['phone_number'],
        }
        serializer = UserInvitationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def send(self, request, *args, **kwargs):
        data = {
            'phone_number': request.data['phone_number']
        }
        codigo = str(random.randint(100000, 999999))
        conn = http.client.HTTPSConnection("m0480.contaboserver.net")
        payload = "{\r\n    \"telefono\":\""+request.data['phone_number'] + \
            "\",\r\n    \"mensaje\":\"Mensaje de confirmacion tax-innova tucodigo es:" + \
            codigo + "\",\r\n    \"servicio\":\"Tax-innova\"\r\n}\r\n"
        headers = {
            'Authorization': 'Basic dGF4aW5ub3ZhdGlvbjpUNHgxbm5vdmEjVHVQYXNz',
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/api/sms/send", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data2 = data.decode("utf-8")[22]
        jsonRespuesta = {'respuesta': data2, 'numero': codigo}

        return Response(jsonRespuesta, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verificaListo(self, request, *args, **kwargs):

        url = "http://35.243.147.1:8000/API/ListoMX/RegistrarUsuario"

        payload = "{\r\n    \"rfc\": \""+request.data['rfc']+"\",\r\n    \"ciec\": \""+request.data['ciec']+"\"\r\n}"
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        resp_dict = json.loads(response.text)
        resp_dict = resp_dict['LISTO']
        json_acceptable_string = resp_dict.replace("'", "\"")
        resp_dict = json.loads(json_acceptable_string)
        # llenar bases de datos con rfc_id y token de listo
        if 'customer_token' not in resp_dict:
            return Response('error', status=status.HTTP_201_CREATED)

        return Response('correct', status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def sendTemplateFisica(self, request, *args, **kwargs):

        webid = "P1LrZjTYkxZHnp3g"
        apikey = "7a792eb717f0a58366ea2c502bcc8d4f"
        services = FirmamexServices(webid, apikey)
        # html_contract = render_to_string(
        #     'contrato/pruebaContrato.html',
        #     {
        #         'message': data['message'],
        #         'user': user
        #     }
        # ) 
        templateData = """ 
        <html>
            <body>
                <div>
                    <p>
                    <img src="data:image/png;base64,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" width="340" height="100">
                    <p>
                    <h2>ESTE CONTRATO LO CELEBRAN POR UNA PARTE INS IMPULSORA DE NEGOCIOS SOSTENIBLES S. DE R.L DE C.V., EN LO SUCESIVO “TAX INNOVA” Y POR LA OTRA PARTE LA PERSONA CUYOS DATOS SE PRECISAN EN EL ANEXO DE DATOS GENERALES, EN LO SUCESIVO “EL CLIENTE”, A QUIENES DE MANERA CONJUNTA SE LES DENOMINARÁ, “LAS PARTES”, DE CONFORMIDAD CON LAS DECLARACIONES Y CLÁUSULAS SIGUIENTES:</h2>
                    <h2>DECLARACIONES</h2>
                    <h4>I.- Declara Tax Innova que:</h4>
                    </p>
                    <p>
                        1.	Es una Sociedad de Responsabilidad Limitada constituida y organizada conforme a las Leyes Mexicanas, con facultad para celebrar este tipo de contratos.
                        <br>
                            2.	Sus datos de identificación son los establecidos en el Anexo de Datos Generales. 
                        <br> 
                            3.	Su representante cuenta con facultades suficientes y necesarias para obligarle en los términos del presente contrato, las cuales no le han sido modificadas o limitadas en forma alguna. 
                        <br>
                            4.	Está en disposición de ofrecer al Cliente los servicios que son objeto de este contrato. 
                        <br>
                            5.	Toda la información que proporciona es real y veraz.
                    <p>
                        <h4>II.- Declara el Cliente que:</h4>
                    </p>
                    <p>
                        1.	Es una persona física con capacidad legal para obligarse en los términos de este contrato o que es representante legal de una persona física y que cuenta con las facultades para celebrar el presente contrato. 
                        <br>
                        2.	Sus datos de identificación son los establecidos en el Anexo de Datos Generales. 
                        <br>
                        3.	Está interesado en que Tax Innova le preste los Servicios objeto de este contrato.
                        <br>
                        4.	Conoce y está de acuerdo con el contenido de este contrato, y que es su voluntad suscribirlo.
                        <br>
                        5.	Toda la información que proporciona es real y veraz
                    </p>
                    <p>
                        <h4>III.- Declaran las Partes que:</h4>
                    </p>
                    <p>
                        1.	Se reconocen la personalidad con la que actúan para celebrar el presente Contrato.
                        <br>
                        2.	El presente Contrato constituye el consentimiento pleno y el acuerdo absoluto de las Partes en relación con el objeto materia del mismo, no existiendo restricciones, promesas, declaraciones, garantías, convenios o compromisos en relación con el objeto de este Contrato, distintos de los expresamente establecidos o mencionadas en él, por lo que reemplaza todos los acuerdos y entendimientos previos entre las Partes con respecto al objeto del mismo.
                        <br>
                        3.	No existe error, dolo ni mala fe.
                        <br>
                        4.	La violación a sus declaraciones implica un incumplimiento sustancial al presente Contrato.
                    </p>
                    <p>
                        <h2>DEFINICIONES</h2>
                    </p>
                    <p>
                        TABLA
                        <br>
                        De conformidad con las declaraciones que anteceden, las Partes están de acuerdo en sujetarse a las siguientes:
                    </p>
                    <p>
                        <h2>CLÁUSULAS</h2>
                    </p>
                    <p>
                        <h4>PRIMERA.- Objeto del contrato</h4>
                    </p>
                    <p>
                        Las Partes celebran un contrato mediante el cual Tax Innova prestará los Servicios al Cliente de acuerdo con el Plan contratado, bajo las modalidades mencionadas en este contrato. 
                        <br>
                        El Cliente acepta contratar el PLAN [nombre del plan] que se señala a continuación:
                        <br>
                        TABLA
                    </p>
                    <p>
                        <h4>SEGUNDA.- Proceso de validación previo a la contratación</h4>
                    </p>
                    <p>
                        1.	Para la contratación del Plan, el Cliente deberá proporcionar a Tax Innova la información solicitada por éste.
                        <br>
                        2.	Tax Innova realizará un Proceso de validación de la información entregada por el Cliente, para asegurar que la misma es verídica. 
                        <br>
                        3.	Si durante el Proceso de validación, Tax Innova advierte que el Cliente entregó información falsa, incluyendo el supuesto de suplantación de identidad, ejercerá las acciones legales conducentes.
                        <br>
                        4.	La entrada en vigor de este contrato estará sujeta a la condición suspensiva consistente en que Tax Innova confirme la veracidad de la información proporcionada por el Cliente, una vez que haya llevado a cabo el Proceso de validación.
                        <br>
                        5.	Tax Innova informará al Cliente el resultado del Proceso de validación a través de los Medios de comunicación proporcionados por el Cliente.
                        <br>
                        6.	La vigencia de este contrato iniciará a partir del momento en que Tax Innova envíe un mensaje al Cliente informándole como “APROBADO” el Proceso de validación, a través de los Medios de comunicación.
                    </p>
                    <p>
                        <h4>TERCERA.- Acceso</h4>
                    </p>
                    <p>
                        1.	El Cliente accederá a los Servicios a través de diversas Claves de acceso, tales como nombre de usuario, contraseña, entre otros. 
                        <br>
                        2.	Las Claves de acceso serán definidos por el Cliente y validados por Tax Innova. [Tax Innova no los conoce, señalar eso] 
                        <br>
                        3.	Tax Innova definirá las características que deberán cumplir las Claves de acceso.
                        <br>
                        4.	Tax Innova podrá establecer medios adicionales de autenticación para asegurarse de la identidad del Cliente.
                        <br>
                        5.	Tax Innova podrá restringir temporalmente el acceso a los Servicios si advierte que hay intetos de fraude.
                        <br>
                        6.	El Cliente es el único responsable y conocedor de la contraseña.
                        <br>
                        7.	Los Servicios serán prestados por Tax Innova en los sitios web www.taxinnovation.mx y www.taxinnova.mx.    
                    </p>
                    <p>
                        <h4>CUARTA.- Objeto</h4>
                    </p>
                    <p>
                        Tax Innova, por este medio se obliga a proporcionar al Cliente, el Servicio, a través de sus propios recursos humanos y materiales, o bien, a través de aquellos que sean necesarios adquirir, arrendar o allegarse por cualquier medio de forma lícita, para el cumplimiento de las obligaciones señaladas en el presente Contrato, así como a efectuar las modificaciones que en cualquier momento fueren necesarias previo acuerdo con el Cliente a los Servicios. 
                        El Servicio será desarrollado por Tax Innova en los sitios web www.taxinnovation.mx y www.taxinnova.mx (Plataforma) a través de sus socios y del personal que emplee o subcontrate. 
                        <br>
                        Para lo anterior, Tax Innova manifiesta y reconoce que es titular de los derechos de propiedad de la Plataforma, y que cuenta con el conocimiento, herramientas y demás necesidades para el buen funcionamiento de los mismos. 
                        <br>   
                    </p>
                    <p>
                        <h4>QUINTA.- Contraprestación y forma de pago</h4>
                    </p>
                    <p>
                        El Cliente pagará a Tax Innova por el Servicio <span class="signmage-template-field" id="tipo_plan"></span>, objeto de este contrato, la cantidad mensual de $ <span class="signmage-template-field" id="precio_plan"></span> pesos, incluyendo el Impuesto al Valor Agregado (IVA) por cada razón social y RFC que dé de alta. 
                        <br>
                        La Contraprestación deberá pagarse de manera mensual el día en que contrate el Servicio realizando un pago que le dará acceso al Servicio de Tax Innova por un período de un mes 
                        <br>
                        El pago se efectuará a través de la Plataforma, a través de los medios que ahí se ofrezcan. 
                        <br>
                        En caso de que Tax Innova no pueda llevar a cabo sus obligaciones por causas no imputables al mismo, el Cliente tendrá la obligación de pagar la Contraprestación conforme a lo señalado en esta cláusula, en el entendido que Tax Innova tendrá que cumplir con sus obligaciones (mutatis mutandis), una vez que el impedimento desaparezca.
                        <br>   
                    </p>
                    <p>
                        <h4>SEXTA.- Responsabilidad laboral</h4>
                    </p>
                    <p>
                        Tax Innova manifiesta que para la prestación del Servicio objeto del presente Contrato utilizará elementos, equipo y recursos humanos y materiales propios, adecuados y suficientes para el cumplimiento de sus obligaciones o, en su caso, de terceros sub-contratados para cumplir con los fines de este instrumento. 
                        <br>
                        Tax Innova, respecto de los trabajadores que emplee o subcontrate, en su caso, para cumplir el objeto del presente Contrato, asume incondicionalmente el carácter de patrón, de conformidad con lo estipulado en el artículo 13 de la Ley Federal del Trabajo.
                        <br>
                        Las Partes acuerdan en que no existirá relación alguna de tipo laboral o de seguridad social entre Tax Innova, su personal, terceros sub-contratados, y el Cliente, toda vez que se trata de una relación comercial conforme a lo dispuesto analógicamente por el artículo 280 del Código de Comercio y por el artículo 13 de la Ley Federal del Trabajo.
                        <br>
                    </p>
                    <p>
                        <h4>SEPTIMA.- Obligaciones de Tax Innova y su personal </h4>
                    </p>
                    <p>
                        Son obligaciones de Tax Innova, las siguientes:
                        <br>
                        1.	Prestar el Servicio de conformidad con lo establecido en el presente Contrato y el Paquete elegido.
                        <br>
                        2.	Garantizar que el Servicio esté libre de defectos y se ajusten a las especificaciones y particularidades de cada uno de los Paquetes, durante toda su vigencia. 
                        <br>
                        3.	Garantizar que el Servicio esté disponible para el Cliente en la Plataforma o en los medios de contacto seleccionados por el Cliente.  
                        <br>
                        4.	Contar y disponer, en todo momento, con personal y recursos que aseguren el correcto y continuo desarrollo y prestación del Servicio.
                        <br>
                        5.	En caso de que exista una interrupción en la prestación del Servicio, informar de manera inmediata al Cliente para que pueda tomar las medidas necesarias y reactivar la prestación del Servicio a la brevedad. 
                        <br>
                        6.	Considerar como confidencial toda la información sobre el Cliente, que llegue a conocer con motivo de la celebración de este Contrato divulgandola unicamente al personal que emplee y/o subcontrate y que necesite conocer dicha información para la prestación del Servicio.
                        <br>
                        7.	Proteger  los datos personales y fiscales del Cliente de acuerdo con lo señalado en el Aviso de Privacidad.
                    </p>
                    <p>
                        <h4>OCTAVA.- Obligaciones del Cliente </h4>
                    </p>
                    <p>
                        Son obligaciones de Tax Innova, las siguientes:
                        <br>
                        1.	Pagar a Tax Innova, en los términos, condiciones y periodicidad pactados en el presente Contrato las cantidades que correspondan por la prestación del Servicio del Paquete elegido.
                        <br>
                        2.	Proporcionar correctamente los datos personales y fiscales solicitados por Tax Innova para llevar a cabo la prestación del Servicio 
                        <br>
                        3.	Notificar a Tax Innova en su domicilio fiscal: Boulevard Manuel Ávila Camacho número 40, oficina 1908, Col. Lomas de Chapultepec,  Alcaldía Miguel Hidalgo, Código Postal 11000, Ciudad de México, por escrito, o mediante el siguiente correo electrónico: contacto@taxinnovation.mx y contacto@taxinnova.mx en un horario de 9:00 a 18:00 horas tan pronto como se originen irregularidades, interrupción o prestación inadecuada y discontinua del Servicio.  
                        <br>
                    </p>
                    <p>
                        <h4>NOVENA.- Confidencialidad </h4>
                    </p>
                    <p>
                        Tax Innova se obliga a considerar como confidencial toda la información sobre el Cliente que obtenga por cualquier medio o motivo o les sea proporcionada aún después de que haya concluido la realización del Servicio, o se haya dado por terminado este Contrato anticipadamente, quedando subsistente su obligación de no revelar la información que haya llegado a conocer por un periodo de 5 (cinco) años después de terminada la relación contractual establecida con el Cliente.
                        <br>
                        Tax Innova podrá divulgar dicha información confidencial únicamente al personal que emplee y/o subcontrate y que necesite conocer dicha información para la prestación del Servicio.
                        <br>
                        La violación a lo establecido en esta Cláusula por alguna de las Partes, pagará los daños y perjuicios que cause a la otra parte.
                        <br>
                        Las obligaciones establecidas para las Partes, en la presente Cláusula, no se aplicarán en los siguientes casos:  
                        <br>
                        a)	Si la información ya era del conocimiento de la parte receptora, en el momento en que fue compartida, lo cual deberá constar mediante sus registros.
                        <br>
                        b)	Que la parte receptora hubiere recibido la misma información de un tercero ajeno a este Contrato y que aquél tenga el derecho de mostrarla.
                        <br>
                        c)	Que la información sea parte del dominio público, por razones no imputables a cualquiera de las Partes.
                        <br>
                        d)  La Información Sujeta de Análisis, se regirá conforme a la Cláusula Décimo Primera siguiente y Décimo Segunda.
                        <br>
                        <br>
                        Una vez concluida la relación consignada en el presente Contrato, las partes se obligan a devolverse entre sí, o a quien sus derechos representen, toda la información y o documentación obtenida y/o proporcionada relacionada con el presente convenio, en un término que no exceda de 7 (siete) días naturales contados a partir de la constancia de terminación respectiva. 
                    </p>
                    <p>
                        <h4>DECIMA.- Vigencia </h4>
                    </p>
                    <p>
                        El presente Contrato tendrá una vigencia por tiempo indefinido, hasta que una de las partes determine darlo por terminado, con una anticipación de 30 (treinta) días naturales a través de un correo electrónico enviado a la cuenta contacto@taxinnova.mx.
                        <br>
                        El plazo mínimo de contratación de un año a partir de la fecha de firma del presente Contrato, y será prorrogado automáticamente por periodo de 1 (un) mes, siempre y cuando las Partes no decidan notificar a la otra parte, por escrito, la no renovación con una anticipación de 5 (cinco) días naturales a la prorrogación automática. 
                        <br>
                    </p>
                    <p>
                        <h4>DECIMA PRIMERA.- Incumplimiento </h4>
                    </p>
                    <p>
                        Si alguna de las Partes incumple alguna de las obligaciones establecidas en el presente Contrato, la otra Parte se lo comunicará por escrito y le otorgará un plazo máximo de 20 (veinte) días naturales para que subsane el incumplimiento correspondiente o manifieste lo que a su derecho convenga.  
                        <br>
                    </p>
                    <p>
                        <h4>DECIMA SEGUNDA.- Terminación anticipada y rescisión </h4>
                    </p>
                    <p>
                        <h4>A)Terminación anticipada </h4>
                    </p>
                    <p>
                        Las Partes podrán dar por terminado el presente Contrato en cualquier momento y sin responsabilidad alguna, siempre y cuando medie aviso por escrito, con 5 (cinco) días naturales de anticipación a la fecha en que deseen que el Contrato deje de surtir sus efectos y estén al corriente con el cumplimiento de sus obligaciones derivadas del presente.   
                        <br>
                    </p>
                    <p>
                        <h4>B)Rescisión. </h4>
                    </p>
                    <p>
                        Las Partes podrán solicitar la rescisión del presente contrato, previo aviso por escrito, en forma inmediata a que tuvo lugar la causal de rescisión, sin necesidad de declaración judicial alguna, a fin de que en un plazo no mayor de 10 (diez) días naturales contados a partir de la fecha de la notificación, la parte notificada exponga lo que a su derecho convenga y demuestre, a juicio y satisfacción de la parte solicitante, que no ha tenido lugar o que se ha subsanado la causal de rescisión. Si transcurrido dicho plazo, la parte notificada no hiciere manifestación alguna, no demuestre que no existió el incumplimiento referido o no lo subsane, el Contrato se tendrá por rescindido de manera inmediata sin responsabilidad alguna para la parte que haya solicitado la rescisión, y sin necesidad de declaración judicial al respecto.   
                        <br>
                        La rescisión del presente Contrato tendrá lugar por cualquiera de las causas siguientes:
                        <br>
                        1.	Cuando la información proporcionada por el Cliente sea incompleta, inexacta o incorrecta, incluyendo los casos de suplantación de identidad. En caso de dolo se estará a lo dispuesto en la Cláusula SEGUNDA.
                        <br>
                        2.	Cuando el Cliente haga mal uso de la información proporcionada por Tax Innova.
                        <br>
                        3.	Incumplimiento de pago por parte del Cliente.
                        <br>
                        4.	Insolvencia evidente de cualquiera de las Partes, declaratoria de concurso mercantil o inicio de un proceso de disolución o liquidación, esto último salvo tratándose de fusiones, reconstituciones o recomposiciones accionarias y de activos.
                        <br>
                        5.	Incumplimiento, por parte de Tax Innova o su personal, incluyendo terceros subcontratados, de prestar el Servicio en los tiempos, términos, y condiciones establecidos en el presente Contrato.
                        <br>
                        <br>
                        En el evento de que exista una terminación anticipada o rescisión imputable a Tax Innova, éste se obliga a reintegrar al Cliente la parte proporcional del pago ya realizado que corresponda al tiempo pendiente por transcurrir posterior a la fecha de terminación, en un término que no exceda de 30 (treinta) días naturales al momento que se decrete la terminación contractual respectiva.
                    </p>
                    <p>
                        <h4>Bloqueo de cuenta </h4>
                    </p>
                    <p>
                        En caso de inactividad en la cuenta del Cliente por un tiempo de 90 (noventa) días naturales, Tax Innova podrá bloquear la cuenta hasta en tanto confirme la identidad del Cliente.   
                        <br>
                        Por comportamiento sospechoso o inusual en la cuenta, Tax Innova podrá bloquear la cuenta hasta que confirme que no existe un intento de uso indebido de la cuenta del Cliente por parte de terceros.
                        <br>
                        Tax Innova enviará mensajes por cualquiera de los medios de comunicación establecidos por el Cliente para confirmar el debido uso de la cuenta del Cliente.
                        <br>
                    </p>
                    <p>
                        <h4>DÉCIMA TERCERA .- Caso Fortuito o Fuerza Mayor</h4>
                    </p>
                    <p>
                        Ninguna de las Partes contratantes es responsable frente a la otra por el incumplimiento en que pudiera incurrir en caso de presentarse un caso fortuito o fuerza mayor y cada una absorberá sus costos en términos de las disposiciones legales aplicables. De presentarse este supuesto, la parte afectada deberá dar aviso a la otra parte del suceso, dentro de un término que no excederá de los cinco días naturales posteriores a la fecha de inicio del evento, para que de común acuerdo determinen las acciones a seguir y, en su caso, la reprogramación correspondiente.   
                        <br>
                    </p>
                    <p>
                        <h4>DÉCIMA CUARTA.- Autorización para el uso de información</h4>
                    </p>
                    <p>
                        Con la contratación de cualquiera de los Servicios, el Cliente autoriza a Tax Innova para que en su nombre y representación, tenga acceso a la información del Cliente que se encuentra en cualquier fuente de información, y para que obtenga la información del Cliente ahí almacenada.   
                        <br>
                        El Cliente autoriza a Tax Innova en los más amplios términos para que utilice dicha información para la prestación de Servicios contratado por el Cliente.
                        <br>
                        Tax Innova no podrá ceder ni compartir con terceros la información del Cliente. El Cliente podrá revocar en cualquier momento la autorización otorgada a Tax Innova en términos de esta cláusula.
                        <br>
                    </p>
                    <p>
                        <h4>DÉCIMA QUINTA.- Información sujeta a análisis</h4>
                    </p>
                    <p>
                        Para que utilice la información proporcionada por el Cliente y la información que se obtendrá descargará de la página del Servicio de Administración Tributaria (SAT). Esta información pertenece al Cliente quien autoriza a Tax Innova para que tenga acceso a dicha información, en adelante, Información Sujeta a Análisis.   
                        <br>
                        En tal virtud, se hace constar que Tax Innova sólo utilizará la Información Sujeta a Análisis para la prestación del Servicio. Tax Innova, en su carácter de Responsable y autorizado por el Cliente, será el único facultado para usar y decidir sobre la Información Sujeta a Análisis bajo los términos del presente contrato.
                        <br>
                        No podrá de forma alguna apropiarse de ni decidir sobre la misma.
                        <br>
                        Durante ese lapso en que Tax Innova tuviere en sus propios sistemas la Información Sujeta a Análisis, será el único responsable de mantener la integridad y confidencialidad de dicha información, estableciendo en sus sistemas las medidas de seguridad pertinentes y necesarias para evitar cualquier mal uso, robo, deterioro o pérdida de la misma.
                        <br>
                        Tax Innova será el único responsable y deberá pagar los daños o perjuicios que se ocasionen al Cliente por la realización de los siguientes actos:
                        <br>
                        	A) Hacer uso de la Información Sujeta a Análisis, excepto de forma agregada y anónima, para fines estadísticos.
                        <br>
                        	B) Copiar y resguardar dicha Información Sujeta a Análisis en sus propios sistemas, salvo por el tiempo que dure la prestación de servicios.
                        <br>
                        	C) Actos que pudieran poner en riesgo la Información Sujeta a Análisis
                        <br>
                        	D) Actos que ocasionen la pérdida, deterioro, robo, falta de integridad, mal uso y/o disponibilidad inapropiada o no autorizada de la Información Sujeta a Análisis.
                    </p>
                    <p>
                        <h4>DÉCIMA SEXTA.- Propiedad intelectual y derechos de autor</h4>
                    </p>
                    <p>
                        Las Partes reconocen y acuerdan que ninguno de los términos y condiciones contenidos en el presente Contrato deberá ser considerado como transmisión de propiedad u otorgamiento de cualquier derecho o licencia de uso, expresa o implícita, respecto de los elementos, datos e información que se proporcionen recíprocamente, tales como marcas, bandas de color, avisos comerciales, nombres comerciales, logotipos o cualquiera otros que constituyan derechos de propiedad intelectual de la otra parte.   
                        <br>
                        En virtud de lo anterior, las Partes se obligan a abstenerse de utilizar en forma alguna la información protegida por propiedad intelectual, sin consentimiento expreso de la propietaria, aun cuando el uso se limite a referencias o exposiciones de carácter comercial, siendo responsable la parte que incumpla con la obligación señalada en esta Cláusula de cubrir la indemnización correspondiente a los últimos 3 (tres) meses de la Contraprestación efectivamente pagada por el Cliente en favor de Tax Innova.
                        <br>
                    </p>
                    <p>
                        <h4>DÉCIMA SÉPTIMA.-  Modificaciones</h4>
                    </p>
                    <p>
                        Para que las modificaciones a los términos y condiciones del presente Contrato o a cualquier aspecto de la prestación del Servicio sean válidas deberán constar en todo momento por escrito y estar debidamente firmadas por el representante legal de cada una de las partes.  
                        <br>
                        <br>
                    </p>
                    <p>
                        <h4>DÉCIMA OCTAVA.-  Notificaciones y comunicaciones</h4>
                    </p>
                    <p>
                        Las Partes acuerdan que las notificaciones y comunicaciones que deseen hacer del conocimiento de la otra parte, deberán ser enviadas por los medios digitales señalados por cada una, en el Apartado de “Declaraciones” del presente contrato. Los cambios de domicilio que efectúen las partes, deberán notificarse, por escrito, mínimo con 15 (quince) días naturales de anticipación a que ocurra el cambio; en caso de que la referida notificación no se efectúe en ese tiempo y forma, se considerará como no efectuada y no surtirá efecto alguno.    
                        <br>
                        Las notificaciones y comunicaciones que se hagan llegar las partes mutuamente, vía correo electrónico, fax u otro medio semejante, para ser válidas y exigibles, deberán ratificarse por la misma vía y en la que pueda constar prueba fehaciente de ello.
                        <br>
                    </p>
                    <p>
                        <h4>DÉCIMA NOVENA.- Cesión de derechos</h4>
                    </p>
                    <p>
                        Las Partes no podrán ceder ni traspasar total o parcialmente los derechos y obligaciones que adquieren a través del presente Contrato, sin la previa autorización otorgada por escrito por la otra parte.    
                        <br>
                        <br>
                    </p>
                    <p>
                        <h4>VIGÉSIMA.- Contratación</h4>
                    </p>
                    <p>
                        Tax Innova podrá contratar a proveedores terceros para la prestación de servicios específicos.    
                        <br>
                        <br>
                    </p>
                    <p>
                        <h4>VIGÉSIMA PRIMERA.- No asociación</h4>
                    </p>
                    <p>
                        El presente Contrato no crea sociedad, asociación ni alguna otra figura jurídica, por lo que cada parte es responsable de sus actos.   
                        <br>
                        <br>
                    </p>
                    <p>
                        <h4>VIGÉSIMA SEGUNDA.- Títulos</h4>
                    </p>
                    <p>
                        Los títulos de las cláusulas del presente Contrato se incluyen en el mismo únicamente como referencias y para conveniencia del lector, por lo que los mismos no afectarán de manera alguna el sentido y alcance de dichas cláusulas.   
                        <br>
                        <br>
                    </p>
                    <p>
                        <h4>VIGÉSIMA TERCERA.- Solución de controversias y jurisdicción</h4>
                    </p>
                    <p>
                        Las Partes acuerdan que, previo al inicio del ejercicio de acciones legales, tratarán de resolver de mutuo acuerdo y con base en el principio de la buena fe de las partes, la situación que dé origen a la controversia, otorgándose mutuamente el plazo de 10 (diez) días naturales posteriores a que se suscite la situación que dé origen a la controversia, para resolver, en la medida de lo posible, dicha situación.    
                        <br>
                        Las Partes acuerdan que, en caso de que no se llegue a acuerdo alguno en términos del primer párrafo de la presente cláusula, cualquier controversia se someterá expresamente a la jurisdicción de los tribunales competentes de la Ciudad de México, por lo que renuncian irrevocablemente a cualquier otro fuero que por razón de sus domicilios presentes o futuros pudiere corresponderles.
                        <br>
                        Enteradas las partes del contenido y alcance legal del presente Contrato, lo firman digitalmente de conformidad en la Ciudad de México, el día <span class="signmage-template-field" id="dia"></span> de <span class="signmage-template-field" id="mes"></span> de <span class="signmage-template-field" id="anno"></span>.
                    </p>
                    /////////////////////////////////////////////////////////////////

                    </p>
                    <h2>ANEXO DE DATOS GENERALES</h2>
                    <br>
                    <h4>1.- Declara Tax Innova que:</h4>
                    <br>
                    <p>
                    1.	Es una Sociedad de Responsabilidad Limitada legalmente constituida de conformidad con las leyes mexicanas, según consta en el testimonio de la escritura pública número 18,335 (dieciocho mil trescientos treinta y cinco) de fecha 18 de marzo del 2011, otorgada ante el Licenciado Moisés Téliz Santoyo, Notario Público número 183 de la Ciudad de México, inscrita ante el Registro Público de la Propiedad y del Comercio de la Ciudad de México, inscrita bajo el folio de personas morales 442740-1 (cuatrocientos cuarenta y dos mil setecientos cuarenta guión uno).
                    </p>
                    <p>
                    2.	Su representante legal es [nombre] quien cuenta con las facultades necesarias para suscribir el presente contrato, según se acredita con la escritura pública mencionada en el inciso a) que antecede; mismas que a la fecha de la presente, no le han sido revocadas, limitadas o modificadas.
                    </p>
                    <p>
                    3.	Que su domicilio fiscal se ubica en Boulevard Manuel Ávila Camacho número 40, oficina 1908, Col. Lomas de Chapultepec, Alcaldía Miguel Hidalgo, Código Postal 11000, Ciudad de México.
                    </p>
                    <p>
                    4.	Su Registro Federal de Contribuyentes es el número IIN-110318-CF2
                    </p>
                    </p>
                </div>
                <br>
                <div>
                    <p>
                    <h4>PARA PERSONA FÍSICA<h/3>
                    <br>
                    <h4>II.A. Declara el Cliente que:</h4>
                    </p>
                </div>
                <div>
                    <p>
                        1.	Que su domicilio fiscal se ubica en <span class="signmage-template-field" id="calle"></span>, <span class="signmage-template-field" id="externalNum"></span>, <span class="signmage-template-field" id="internalNum"></span>, <span class="signmage-template-field" id="colonia"></span>, <span class="signmage-template-field" id="municipio"></span>, <span class="signmage-template-field" id="codpos"></span>, [ciudad], <span class="signmage-template-field" id="estado"></span>. 
                    </p>
                    <p>
                        2.	Que su Registro Federal de Contribuyentes es <span class="signmage-template-field" id="rfc"></span>
                    </p>
                    <p>
                        3.	Que toda la información que proporciona es real y veraz
                    </p>
                    <br>
                    <br>
                    <br>
                    <br>
                    <br>
                    <br>
                    .
                </div>
            </body>
        </html>
        """

        response = services.saveTemplate({
            "template_type": 'html',
            "template_data": base64.b64encode(templateData.encode('utf8')).decode('utf8'),
            "template_name": 'personaFisica'
        })

        return Response(response, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def sendTemplateMoral(self, request, *args, **kwargs):

        webid = "P1LrZjTYkxZHnp3g"
        apikey = "7a792eb717f0a58366ea2c502bcc8d4f"
        services = FirmamexServices(webid, apikey)

        templateData = """ 
        <html>
            <body>
                <div>
                    <p>
                    <img src="data:image/png;base64,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" width="340" height="100">
                    <p>
                    <h2>ESTE CONTRATO LO CELEBRAN POR UNA PARTE INS IMPULSORA DE NEGOCIOS SOSTENIBLES S. DE R.L DE C.V., EN LO SUCESIVO “TAX INNOVA” Y POR LA OTRA PARTE LA PERSONA CUYOS DATOS SE PRECISAN EN EL ANEXO DE DATOS GENERALES, EN LO SUCESIVO “EL CLIENTE”, A QUIENES DE MANERA CONJUNTA SE LES DENOMINARÁ, “LAS PARTES”, DE CONFORMIDAD CON LAS DECLARACIONES Y CLÁUSULAS SIGUIENTES:</h2>
                    <h2>DECLARACIONES</h2>
                    <h4>I.- Declara Tax Innova que:</h4>
                    </p>
                    <p>
                        1.	Es una Sociedad de Responsabilidad Limitada constituida y organizada conforme a las Leyes Mexicanas, con facultad para celebrar este tipo de contratos.
                        <br>
                            2.	Sus datos de identificación son los establecidos en el Anexo de Datos Generales. 
                        <br> 
                            3.	Su representante cuenta con facultades suficientes y necesarias para obligarle en los términos del presente contrato, las cuales no le han sido modificadas o limitadas en forma alguna. 
                        <br>
                            4.	Está en disposición de ofrecer al Cliente los servicios que son objeto de este contrato. 
                        <br>
                            5.	Toda la información que proporciona es real y veraz.
                    <p>
                        <h4>II.- Declara el Cliente que:</h4>
                    </p>
                    <p>
                        1.	Es una persona física con capacidad legal para obligarse en los términos de este contrato o que es representante legal de una persona física y que cuenta con las facultades para celebrar el presente contrato. 
                        <br>
                        2.	Sus datos de identificación son los establecidos en el Anexo de Datos Generales. 
                        <br>
                        3.	Está interesado en que Tax Innova le preste los Servicios objeto de este contrato.
                        <br>
                        4.	Conoce y está de acuerdo con el contenido de este contrato, y que es su voluntad suscribirlo.
                        <br>
                        5.	Toda la información que proporciona es real y veraz
                    </p>
                    <p>
                        <h4>III.- Declaran las Partes que:</h4>
                    </p>
                    <p>
                        1.	Se reconocen la personalidad con la que actúan para celebrar el presente Contrato.
                        <br>
                        2.	El presente Contrato constituye el consentimiento pleno y el acuerdo absoluto de las Partes en relación con el objeto materia del mismo, no existiendo restricciones, promesas, declaraciones, garantías, convenios o compromisos en relación con el objeto de este Contrato, distintos de los expresamente establecidos o mencionadas en él, por lo que reemplaza todos los acuerdos y entendimientos previos entre las Partes con respecto al objeto del mismo.
                        <br>
                        3.	No existe error, dolo ni mala fe.
                        <br>
                        4.	La violación a sus declaraciones implica un incumplimiento sustancial al presente Contrato.
                    </p>
                    <p>
                        <h2>DEFINICIONES</h2>
                    </p>
                    <p>
                        TABLA
                        <br>
                        De conformidad con las declaraciones que anteceden, las Partes están de acuerdo en sujetarse a las siguientes:
                    </p>
                    <p>
                        <h2>CLÁUSULAS</h2>
                    </p>
                    <p>
                        <h4>PRIMERA.- Objeto del contrato</h4>
                    </p>
                    <p>
                        Las Partes celebran un contrato mediante el cual Tax Innova prestará los Servicios al Cliente de acuerdo con el Plan contratado, bajo las modalidades mencionadas en este contrato. 
                        <br>
                        El Cliente acepta contratar el PLAN [nombre del plan] que se señala a continuación:
                        <br>
                        TABLA
                    </p>
                    <p>
                        <h4>SEGUNDA.- Proceso de validación previo a la contratación</h4>
                    </p>
                    <p>
                        1.	Para la contratación del Plan, el Cliente deberá proporcionar a Tax Innova la información solicitada por éste.
                        <br>
                        2.	Tax Innova realizará un Proceso de validación de la información entregada por el Cliente, para asegurar que la misma es verídica. 
                        <br>
                        3.	Si durante el Proceso de validación, Tax Innova advierte que el Cliente entregó información falsa, incluyendo el supuesto de suplantación de identidad, ejercerá las acciones legales conducentes.
                        <br>
                        4.	La entrada en vigor de este contrato estará sujeta a la condición suspensiva consistente en que Tax Innova confirme la veracidad de la información proporcionada por el Cliente, una vez que haya llevado a cabo el Proceso de validación.
                        <br>
                        5.	Tax Innova informará al Cliente el resultado del Proceso de validación a través de los Medios de comunicación proporcionados por el Cliente.
                        <br>
                        6.	La vigencia de este contrato iniciará a partir del momento en que Tax Innova envíe un mensaje al Cliente informándole como “APROBADO” el Proceso de validación, a través de los Medios de comunicación.
                    </p>
                    <p>
                        <h4>TERCERA.- Acceso</h4>
                    </p>
                    <p>
                        1.	El Cliente accederá a los Servicios a través de diversas Claves de acceso, tales como nombre de usuario, contraseña, entre otros. 
                        <br>
                        2.	Las Claves de acceso serán definidos por el Cliente y validados por Tax Innova. [Tax Innova no los conoce, señalar eso] 
                        <br>
                        3.	Tax Innova definirá las características que deberán cumplir las Claves de acceso.
                        <br>
                        4.	Tax Innova podrá establecer medios adicionales de autenticación para asegurarse de la identidad del Cliente.
                        <br>
                        5.	Tax Innova podrá restringir temporalmente el acceso a los Servicios si advierte que hay intetos de fraude.
                        <br>
                        6.	El Cliente es el único responsable y conocedor de la contraseña.
                        <br>
                        7.	Los Servicios serán prestados por Tax Innova en los sitios web www.taxinnovation.mx y www.taxinnova.mx.    
                    </p>
                    <p>
                        <h4>CUARTA.- Objeto</h4>
                    </p>
                    <p>
                        Tax Innova, por este medio se obliga a proporcionar al Cliente, el Servicio, a través de sus propios recursos humanos y materiales, o bien, a través de aquellos que sean necesarios adquirir, arrendar o allegarse por cualquier medio de forma lícita, para el cumplimiento de las obligaciones señaladas en el presente Contrato, así como a efectuar las modificaciones que en cualquier momento fueren necesarias previo acuerdo con el Cliente a los Servicios. 
                        El Servicio será desarrollado por Tax Innova en los sitios web www.taxinnovation.mx y www.taxinnova.mx (Plataforma) a través de sus socios y del personal que emplee o subcontrate. 
                        <br>
                        Para lo anterior, Tax Innova manifiesta y reconoce que es titular de los derechos de propiedad de la Plataforma, y que cuenta con el conocimiento, herramientas y demás necesidades para el buen funcionamiento de los mismos. 
                        <br>   
                    </p>
                    <p>
                        <h4>QUINTA.- Contraprestación y forma de pago</h4>
                    </p>
                    <p>
                        El Cliente pagará a Tax Innova por el Servicio ______(FREEMIUM, BÁSICO o PREMIUM), objeto de este contrato, la cantidad mensual de $_______, incluyendo el Impuesto al Valor Agregado (IVA) por cada razón social y RFC que dé de alta. 
                        <br>
                        La Contraprestación deberá pagarse de manera mensual el día en que contrate el Servicio realizando un pago que le dará acceso al Servicio de Tax Innova por un período de un mes 
                        <br>
                        El pago se efectuará a través de la Plataforma, a través de los medios que ahí se ofrezcan. 
                        <br>
                        En caso de que Tax Innova no pueda llevar a cabo sus obligaciones por causas no imputables al mismo, el Cliente tendrá la obligación de pagar la Contraprestación conforme a lo señalado en esta cláusula, en el entendido que Tax Innova tendrá que cumplir con sus obligaciones (mutatis mutandis), una vez que el impedimento desaparezca.
                        <br>   
                    </p>
                    <p>
                        <h4>SEXTA.- Responsabilidad laboral</h4>
                    </p>
                    <p>
                        Tax Innova manifiesta que para la prestación del Servicio objeto del presente Contrato utilizará elementos, equipo y recursos humanos y materiales propios, adecuados y suficientes para el cumplimiento de sus obligaciones o, en su caso, de terceros sub-contratados para cumplir con los fines de este instrumento. 
                        <br>
                        Tax Innova, respecto de los trabajadores que emplee o subcontrate, en su caso, para cumplir el objeto del presente Contrato, asume incondicionalmente el carácter de patrón, de conformidad con lo estipulado en el artículo 13 de la Ley Federal del Trabajo.
                        <br>
                        Las Partes acuerdan en que no existirá relación alguna de tipo laboral o de seguridad social entre Tax Innova, su personal, terceros sub-contratados, y el Cliente, toda vez que se trata de una relación comercial conforme a lo dispuesto analógicamente por el artículo 280 del Código de Comercio y por el artículo 13 de la Ley Federal del Trabajo.
                        <br>
                    </p>
                    <p>
                        <h4>SEPTIMA.- Obligaciones de Tax Innova y su personal </h4>
                    </p>
                    <p>
                        Son obligaciones de Tax Innova, las siguientes:
                        <br>
                        1.	Prestar el Servicio de conformidad con lo establecido en el presente Contrato y el Paquete elegido.
                        <br>
                        2.	Garantizar que el Servicio esté libre de defectos y se ajusten a las especificaciones y particularidades de cada uno de los Paquetes, durante toda su vigencia. 
                        <br>
                        3.	Garantizar que el Servicio esté disponible para el Cliente en la Plataforma o en los medios de contacto seleccionados por el Cliente.  
                        <br>
                        4.	Contar y disponer, en todo momento, con personal y recursos que aseguren el correcto y continuo desarrollo y prestación del Servicio.
                        <br>
                        5.	En caso de que exista una interrupción en la prestación del Servicio, informar de manera inmediata al Cliente para que pueda tomar las medidas necesarias y reactivar la prestación del Servicio a la brevedad. 
                        <br>
                        6.	Considerar como confidencial toda la información sobre el Cliente, que llegue a conocer con motivo de la celebración de este Contrato divulgandola unicamente al personal que emplee y/o subcontrate y que necesite conocer dicha información para la prestación del Servicio.
                        <br>
                        7.	Proteger  los datos personales y fiscales del Cliente de acuerdo con lo señalado en el Aviso de Privacidad.
                    </p>
                    <p>
                        <h4>OCTAVA.- Obligaciones del Cliente </h4>
                    </p>
                    <p>
                        Son obligaciones de Tax Innova, las siguientes:
                        <br>
                        1.	Pagar a Tax Innova, en los términos, condiciones y periodicidad pactados en el presente Contrato las cantidades que correspondan por la prestación del Servicio del Paquete elegido.
                        <br>
                        2.	Proporcionar correctamente los datos personales y fiscales solicitados por Tax Innova para llevar a cabo la prestación del Servicio 
                        <br>
                        3.	Notificar a Tax Innova en su domicilio fiscal: Boulevard Manuel Ávila Camacho número 40, oficina 1908, Col. Lomas de Chapultepec,  Alcaldía Miguel Hidalgo, Código Postal 11000, Ciudad de México, por escrito, o mediante el siguiente correo electrónico: contacto@taxinnovation.mx y contacto@taxinnova.mx en un horario de 9:00 a 18:00 horas tan pronto como se originen irregularidades, interrupción o prestación inadecuada y discontinua del Servicio.  
                        <br>
                    </p>
                    <p>
                        <h4>NOVENA.- Confidencialidad </h4>
                    </p>
                    <p>
                        Tax Innova se obliga a considerar como confidencial toda la información sobre el Cliente que obtenga por cualquier medio o motivo o les sea proporcionada aún después de que haya concluido la realización del Servicio, o se haya dado por terminado este Contrato anticipadamente, quedando subsistente su obligación de no revelar la información que haya llegado a conocer por un periodo de 5 (cinco) años después de terminada la relación contractual establecida con el Cliente.
                        <br>
                        Tax Innova podrá divulgar dicha información confidencial únicamente al personal que emplee y/o subcontrate y que necesite conocer dicha información para la prestación del Servicio.
                        <br>
                        La violación a lo establecido en esta Cláusula por alguna de las Partes, pagará los daños y perjuicios que cause a la otra parte.
                        <br>
                        Las obligaciones establecidas para las Partes, en la presente Cláusula, no se aplicarán en los siguientes casos:  
                        <br>
                        a)	Si la información ya era del conocimiento de la parte receptora, en el momento en que fue compartida, lo cual deberá constar mediante sus registros.
                        <br>
                        b)	Que la parte receptora hubiere recibido la misma información de un tercero ajeno a este Contrato y que aquél tenga el derecho de mostrarla.
                        <br>
                        c)	Que la información sea parte del dominio público, por razones no imputables a cualquiera de las Partes.
                        <br>
                        d)  La Información Sujeta de Análisis, se regirá conforme a la Cláusula Décimo Primera siguiente y Décimo Segunda.
                        <br>
                        <br>
                        Una vez concluida la relación consignada en el presente Contrato, las partes se obligan a devolverse entre sí, o a quien sus derechos representen, toda la información y o documentación obtenida y/o proporcionada relacionada con el presente convenio, en un término que no exceda de 7 (siete) días naturales contados a partir de la constancia de terminación respectiva. 
                    </p>
                    <p>
                        <h4>DECIMA.- Vigencia </h4>
                    </p>
                    <p>
                        El presente Contrato tendrá una vigencia por tiempo indefinido, hasta que una de las partes determine darlo por terminado, con una anticipación de 30 (treinta) días naturales a través de un correo electrónico enviado a la cuenta contacto@taxinnova.mx.
                        <br>
                        El plazo mínimo de contratación de un año a partir de la fecha de firma del presente Contrato, y será prorrogado automáticamente por periodo de 1 (un) mes, siempre y cuando las Partes no decidan notificar a la otra parte, por escrito, la no renovación con una anticipación de 5 (cinco) días naturales a la prorrogación automática. 
                        <br>
                    </p>
                    <p>
                        <h4>DECIMA PRIMERA.- Incumplimiento </h4>
                    </p>
                    <p>
                        Si alguna de las Partes incumple alguna de las obligaciones establecidas en el presente Contrato, la otra Parte se lo comunicará por escrito y le otorgará un plazo máximo de 20 (veinte) días naturales para que subsane el incumplimiento correspondiente o manifieste lo que a su derecho convenga.  
                        <br>
                    </p>
                    <p>
                        <h4>DECIMA SEGUNDA.- Terminación anticipada y rescisión </h4>
                    </p>
                    <p>
                        <h4>A)Terminación anticipada </h4>
                    </p>
                    <p>
                        Las Partes podrán dar por terminado el presente Contrato en cualquier momento y sin responsabilidad alguna, siempre y cuando medie aviso por escrito, con 5 (cinco) días naturales de anticipación a la fecha en que deseen que el Contrato deje de surtir sus efectos y estén al corriente con el cumplimiento de sus obligaciones derivadas del presente.   
                        <br>
                    </p>
                    <p>
                        <h4>B)Rescisión. </h4>
                    </p>
                    <p>
                        Las Partes podrán solicitar la rescisión del presente contrato, previo aviso por escrito, en forma inmediata a que tuvo lugar la causal de rescisión, sin necesidad de declaración judicial alguna, a fin de que en un plazo no mayor de 10 (diez) días naturales contados a partir de la fecha de la notificación, la parte notificada exponga lo que a su derecho convenga y demuestre, a juicio y satisfacción de la parte solicitante, que no ha tenido lugar o que se ha subsanado la causal de rescisión. Si transcurrido dicho plazo, la parte notificada no hiciere manifestación alguna, no demuestre que no existió el incumplimiento referido o no lo subsane, el Contrato se tendrá por rescindido de manera inmediata sin responsabilidad alguna para la parte que haya solicitado la rescisión, y sin necesidad de declaración judicial al respecto.   
                        <br>
                        La rescisión del presente Contrato tendrá lugar por cualquiera de las causas siguientes:
                        <br>
                        1.	Cuando la información proporcionada por el Cliente sea incompleta, inexacta o incorrecta, incluyendo los casos de suplantación de identidad. En caso de dolo se estará a lo dispuesto en la Cláusula SEGUNDA.
                        <br>
                        2.	Cuando el Cliente haga mal uso de la información proporcionada por Tax Innova.
                        <br>
                        3.	Incumplimiento de pago por parte del Cliente.
                        <br>
                        4.	Insolvencia evidente de cualquiera de las Partes, declaratoria de concurso mercantil o inicio de un proceso de disolución o liquidación, esto último salvo tratándose de fusiones, reconstituciones o recomposiciones accionarias y de activos.
                        <br>
                        5.	Incumplimiento, por parte de Tax Innova o su personal, incluyendo terceros subcontratados, de prestar el Servicio en los tiempos, términos, y condiciones establecidos en el presente Contrato.
                        <br>
                        <br>
                        En el evento de que exista una terminación anticipada o rescisión imputable a Tax Innova, éste se obliga a reintegrar al Cliente la parte proporcional del pago ya realizado que corresponda al tiempo pendiente por transcurrir posterior a la fecha de terminación, en un término que no exceda de 30 (treinta) días naturales al momento que se decrete la terminación contractual respectiva.
                    </p>
                    <p>
                        <h4>Bloqueo de cuenta </h4>
                    </p>
                    <p>
                        En caso de inactividad en la cuenta del Cliente por un tiempo de 90 (noventa) días naturales, Tax Innova podrá bloquear la cuenta hasta en tanto confirme la identidad del Cliente.   
                        <br>
                        Por comportamiento sospechoso o inusual en la cuenta, Tax Innova podrá bloquear la cuenta hasta que confirme que no existe un intento de uso indebido de la cuenta del Cliente por parte de terceros.
                        <br>
                        Tax Innova enviará mensajes por cualquiera de los medios de comunicación establecidos por el Cliente para confirmar el debido uso de la cuenta del Cliente.
                        <br>
                    </p>
                    <p>
                        <h4>DÉCIMA TERCERA .- Caso Fortuito o Fuerza Mayor</h4>
                    </p>
                    <p>
                        Ninguna de las Partes contratantes es responsable frente a la otra por el incumplimiento en que pudiera incurrir en caso de presentarse un caso fortuito o fuerza mayor y cada una absorberá sus costos en términos de las disposiciones legales aplicables. De presentarse este supuesto, la parte afectada deberá dar aviso a la otra parte del suceso, dentro de un término que no excederá de los cinco días naturales posteriores a la fecha de inicio del evento, para que de común acuerdo determinen las acciones a seguir y, en su caso, la reprogramación correspondiente.   
                        <br>
                    </p>
                    <p>
                        <h4>DÉCIMA CUARTA.- Autorización para el uso de información</h4>
                    </p>
                    <p>
                        Con la contratación de cualquiera de los Servicios, el Cliente autoriza a Tax Innova para que en su nombre y representación, tenga acceso a la información del Cliente que se encuentra en cualquier fuente de información, y para que obtenga la información del Cliente ahí almacenada.   
                        <br>
                        El Cliente autoriza a Tax Innova en los más amplios términos para que utilice dicha información para la prestación de Servicios contratado por el Cliente.
                        <br>
                        Tax Innova no podrá ceder ni compartir con terceros la información del Cliente. El Cliente podrá revocar en cualquier momento la autorización otorgada a Tax Innova en términos de esta cláusula.
                        <br>
                    </p>
                    <p>
                        <h4>DÉCIMA QUINTA.- Información sujeta a análisis</h4>
                    </p>
                    <p>
                        Para que utilice la información proporcionada por el Cliente y la información que se obtendrá descargará de la página del Servicio de Administración Tributaria (SAT). Esta información pertenece al Cliente quien autoriza a Tax Innova para que tenga acceso a dicha información, en adelante, Información Sujeta a Análisis.   
                        <br>
                        En tal virtud, se hace constar que Tax Innova sólo utilizará la Información Sujeta a Análisis para la prestación del Servicio. Tax Innova, en su carácter de Responsable y autorizado por el Cliente, será el único facultado para usar y decidir sobre la Información Sujeta a Análisis bajo los términos del presente contrato.
                        <br>
                        No podrá de forma alguna apropiarse de ni decidir sobre la misma.
                        <br>
                        Durante ese lapso en que Tax Innova tuviere en sus propios sistemas la Información Sujeta a Análisis, será el único responsable de mantener la integridad y confidencialidad de dicha información, estableciendo en sus sistemas las medidas de seguridad pertinentes y necesarias para evitar cualquier mal uso, robo, deterioro o pérdida de la misma.
                        <br>
                        Tax Innova será el único responsable y deberá pagar los daños o perjuicios que se ocasionen al Cliente por la realización de los siguientes actos:
                        <br>
                        	A) Hacer uso de la Información Sujeta a Análisis, excepto de forma agregada y anónima, para fines estadísticos.
                        <br>
                        	B) Copiar y resguardar dicha Información Sujeta a Análisis en sus propios sistemas, salvo por el tiempo que dure la prestación de servicios.
                        <br>
                        	C) Actos que pudieran poner en riesgo la Información Sujeta a Análisis
                        <br>
                        	D) Actos que ocasionen la pérdida, deterioro, robo, falta de integridad, mal uso y/o disponibilidad inapropiada o no autorizada de la Información Sujeta a Análisis.
                    </p>
                    <p>
                        <h4>DÉCIMA SEXTA.- Propiedad intelectual y derechos de autor</h4>
                    </p>
                    <p>
                        Las Partes reconocen y acuerdan que ninguno de los términos y condiciones contenidos en el presente Contrato deberá ser considerado como transmisión de propiedad u otorgamiento de cualquier derecho o licencia de uso, expresa o implícita, respecto de los elementos, datos e información que se proporcionen recíprocamente, tales como marcas, bandas de color, avisos comerciales, nombres comerciales, logotipos o cualquiera otros que constituyan derechos de propiedad intelectual de la otra parte.   
                        <br>
                        En virtud de lo anterior, las Partes se obligan a abstenerse de utilizar en forma alguna la información protegida por propiedad intelectual, sin consentimiento expreso de la propietaria, aun cuando el uso se limite a referencias o exposiciones de carácter comercial, siendo responsable la parte que incumpla con la obligación señalada en esta Cláusula de cubrir la indemnización correspondiente a los últimos 3 (tres) meses de la Contraprestación efectivamente pagada por el Cliente en favor de Tax Innova.
                        <br>
                    </p>
                    <p>
                        <h4>DÉCIMA SÉPTIMA.-  Modificaciones</h4>
                    </p>
                    <p>
                        Para que las modificaciones a los términos y condiciones del presente Contrato o a cualquier aspecto de la prestación del Servicio sean válidas deberán constar en todo momento por escrito y estar debidamente firmadas por el representante legal de cada una de las partes.  
                        <br>
                        <br>
                    </p>
                    <p>
                        <h4>DÉCIMA OCTAVA.-  Notificaciones y comunicaciones</h4>
                    </p>
                    <p>
                        Las Partes acuerdan que las notificaciones y comunicaciones que deseen hacer del conocimiento de la otra parte, deberán ser enviadas por los medios digitales señalados por cada una, en el Apartado de “Declaraciones” del presente contrato. Los cambios de domicilio que efectúen las partes, deberán notificarse, por escrito, mínimo con 15 (quince) días naturales de anticipación a que ocurra el cambio; en caso de que la referida notificación no se efectúe en ese tiempo y forma, se considerará como no efectuada y no surtirá efecto alguno.    
                        <br>
                        Las notificaciones y comunicaciones que se hagan llegar las partes mutuamente, vía correo electrónico, fax u otro medio semejante, para ser válidas y exigibles, deberán ratificarse por la misma vía y en la que pueda constar prueba fehaciente de ello.
                        <br>
                    </p>
                    <p>
                        <h4>DÉCIMA NOVENA.- Cesión de derechos</h4>
                    </p>
                    <p>
                        Las Partes no podrán ceder ni traspasar total o parcialmente los derechos y obligaciones que adquieren a través del presente Contrato, sin la previa autorización otorgada por escrito por la otra parte.    
                        <br>
                        <br>
                    </p>
                    <p>
                        <h4>VIGÉSIMA.- Contratación</h4>
                    </p>
                    <p>
                        Tax Innova podrá contratar a proveedores terceros para la prestación de servicios específicos.    
                        <br>
                        <br>
                    </p>
                    <p>
                        <h4>VIGÉSIMA PRIMERA.- No asociación</h4>
                    </p>
                    <p>
                        El presente Contrato no crea sociedad, asociación ni alguna otra figura jurídica, por lo que cada parte es responsable de sus actos.   
                        <br>
                        <br>
                    </p>
                    <p>
                        <h4>VIGÉSIMA SEGUNDA.- Títulos</h4>
                    </p>
                    <p>
                        Los títulos de las cláusulas del presente Contrato se incluyen en el mismo únicamente como referencias y para conveniencia del lector, por lo que los mismos no afectarán de manera alguna el sentido y alcance de dichas cláusulas.   
                        <br>
                        <br>
                    </p>
                    <p>
                        <h4>VIGÉSIMA TERCERA.- Solución de controversias y jurisdicción</h4>
                    </p>
                    <p>
                        Las Partes acuerdan que, previo al inicio del ejercicio de acciones legales, tratarán de resolver de mutuo acuerdo y con base en el principio de la buena fe de las partes, la situación que dé origen a la controversia, otorgándose mutuamente el plazo de 10 (diez) días naturales posteriores a que se suscite la situación que dé origen a la controversia, para resolver, en la medida de lo posible, dicha situación.    
                        <br>
                        Las Partes acuerdan que, en caso de que no se llegue a acuerdo alguno en términos del primer párrafo de la presente cláusula, cualquier controversia se someterá expresamente a la jurisdicción de los tribunales competentes de la Ciudad de México, por lo que renuncian irrevocablemente a cualquier otro fuero que por razón de sus domicilios presentes o futuros pudiere corresponderles.
                        <br>
                        Enteradas las partes del contenido y alcance legal del presente Contrato, lo firman digitalmente de conformidad en la Ciudad de México, el día __ de ________ de 20__.
                    </p>
                    /////////////////////////////////////////////////////////////////

                    </p>
                    <h2>ANEXO DE DATOS GENERALES</h2>
                    <br>
                    <h4>1.- Declara Tax Innova que:</h4>
                    <br>
                    <p>
                    1.	Es una Sociedad de Responsabilidad Limitada legalmente constituida de conformidad con las leyes mexicanas, según consta en el testimonio de la escritura pública número 18,335 (dieciocho mil trescientos treinta y cinco) de fecha 18 de marzo del 2011, otorgada ante el Licenciado Moisés Téliz Santoyo, Notario Público número 183 de la Ciudad de México, inscrita ante el Registro Público de la Propiedad y del Comercio de la Ciudad de México, inscrita bajo el folio de personas morales 442740-1 (cuatrocientos cuarenta y dos mil setecientos cuarenta guión uno).
                    </p>
                    <p>
                    2.	Su representante legal es [nombre] quien cuenta con las facultades necesarias para suscribir el presente contrato, según se acredita con la escritura pública mencionada en el inciso a) que antecede; mismas que a la fecha de la presente, no le han sido revocadas, limitadas o modificadas.
                    </p>
                    <p>
                    3.	Que su domicilio fiscal se ubica en Boulevard Manuel Ávila Camacho número 40, oficina 1908, Col. Lomas de Chapultepec, Alcaldía Miguel Hidalgo, Código Postal 11000, Ciudad de México.
                    </p>
                    <p>
                    4.	Su Registro Federal de Contribuyentes es el número ______________________
                    </p>
                    </p>
                </div>
                <br>
                <div>
                    <p>
                    <h4>PARA PERSONA MORAL<h/3>
                    <br>
                    <h4>II.B. Declara el Cliente por conducto de su apoderado legal que:</h4>
                    </p>
                </div>
                <div>
                    <p>
                        1.	Es una Sociedad Mercantil, denominada ______, debidamente constituida y válidamente existente de conformidad con las leyes mexicanas; según consta en la escritura pública número ______ el día ______ de ______ de ______, ante la fe del Licenciado ______, titular de Notario Público número ______ de la ______ (antes Distrito Federal) inscrita en el Registro Público de la Propiedad y del Comercio de ______, bajo el Folio Mercantil número ______, del día ______ . 
                    </p>
                    <p>
                        2.	Su representante legal es [nombre] quien cuenta con las facultades necesarias para suscribir el presente contrato, según se acredita con la escritura pública número ______, de fecha ______, otorgada ante la fe del Licenciado ______, Notario Público número __ de la Ciudad ___, facultades que no les han sido revocadas, modificadas o limitadas en forma alguna que afecten la validez del presente instrumento.
                    </p>
                    <p>
                        2.	Que su domicilio fiscal se ubica en <span class="signmage-template-field" id="calle"></span>, <span class="signmage-template-field" id="externalNum"></span>, <span class="signmage-template-field" id="internalNum"></span>, <span class="signmage-template-field" id="colonia"></span>, <span class="signmage-template-field" id="municipio"></span>, <span class="signmage-template-field" id="codpos"></span>, [ciudad], <span class="signmage-template-field" id="estado"></span>. 
                    </p>
                    <p>
                        3.	Que su Registro Federal de Contribuyentes es <span class="signmage-template-field" id="rfc"></span>
                    </p>
                </div>
                <br>
                <div>
                    <p>
                    <h4>LINKS DE PAPELES<h/3>
                    <br>
                    </p>
                </div>
                <div>
                    <p>
                        1.	INE ANVERSO
                        <br>
                        https://storage.googleapis.com/tax-innovation-prod/media/<span class="signmage-template-field" id="inefront"></span>
                    </p>
                    <p>
                        2.	INE REVERSO 
                        <br>
                        https://storage.googleapis.com/tax-innovation-prod/media/<span class="signmage-template-field" id="ineback"></span>
                    </p>
                    <p>
                        3.	Comprobante Domicilio
                        <br>
                        https://storage.googleapis.com/tax-innovation-prod/media/<span class="signmage-template-field" id="domicilio"></span>
                    </p>
                    <p>
                        4.	Curp
                        <br>
                        https://storage.googleapis.com/tax-innovation-prod/media/<span class="signmage-template-field" id="curp"></span>
                    </p>
                </div>
            </body>
        </html>
        """

        response = services.saveTemplate({
            "template_type": 'html',
            "template_data": base64.b64encode(templateData.encode('utf8')).decode('utf8'),
            "template_name": 'personaMoral'
        })

        return Response(response, status=status.HTTP_201_CREATED)
    # Rember where @watcher has been removed
    @action(detail=False, methods=['post'])
    def send_template_fields(self, request, *args, **kwargs):

        now = datetime.datetime.now()
        unaSemana = now + datetime.timedelta(days=7)

        webid = "P1LrZjTYkxZHnp3g"
        apikey = "7a792eb717f0a58366ea2c502bcc8d4f"
        services = FirmamexServices(webid, apikey)

        address_one = request.data['address']
        address = address_one['postal_code']
        userprof = request.data['userprofile']

        if userprof['kind_of_person'] == 'PF':
            tipo_contrato = 'personaFisica'
        else:
            tipo_contrato = 'personaMoral'

        tipo_plan = ''
        precio = 0

        if request.data['plan'] == 'gratuito':
            tipo_plan = 'gratuito'
            precio = 0
        elif request.data['plan'] == 'basico':
            tipo_plan = 'basico'
            precio = 300
        elif request.data['plan'] == 'plata':
            tipo_plan = 'plata'
            precio = 800
        elif request.data['plan'] == 'oro':
            tipo_plan = 'oro'
            precio = 2000

        queryset = UserProfile.objects.filter(rfc=userprof['rfc'])

        ine_front = queryset[0].official_identification_front
        ine_back = queryset[0].official_identification_back
        acta_constitutiva = queryset[0].constitutive_act
        authority_doc = queryset[0].authority_doc
        curp = queryset[0].curp
        comprobante_domicilio = queryset[0].proof_of_address

        response = services.request({
            "template_title": tipo_contrato,
            "fields": [
                {
                    "id": "nombre",
                    "value": request.data['name'],
                },
                {
                    "id": "apellidoPaterno",
                    "value": request.data['last_name'],
                },
                {
                    "id": "apellidoMaterno",
                    "value": request.data['second_last_name'],
                },
                {
                    "id": "mail",
                    "value": request.data['email'],
                },
                {
                    "id": "telefono",
                    "value": request.data['phone_number'],
                },
                {
                    "id": "calle",
                    "value": address_one['street'],
                },
                {
                    "id": "colonia",
                    "value": (address['settlement']),
                },
                {
                    "id": "estado",
                    "value": address['estate'],
                },
                {
                    "id": "municipio",
                    "value": address['municipality'],
                },
                {
                    "id": "codpos",
                    "value": address['postal_code'],
                },
                {
                    "id": "internalNum",
                    "value": address_one['internal_num'],
                },
                {
                    "id": "externalNum",
                    "value": address_one['external_num'],
                },
                {
                    "id": "rfc",
                    "value": userprof['rfc'],
                },
                {
                    "id": "dia",
                    "value": str(now.day),
                },
                {
                    "id": "mes",
                    "value": str(now.month),
                },
                {
                    "id": "anno",
                    "value": str(now.year),
                },
                {
                    "id": "tipo_plan",
                    "value": str(tipo_plan),
                },
                {
                    "id": "precio_plan",
                    "value": str(precio),
                },
            ],
            "stickers": [{
                "authority": "Vinculada a Correo Electronico por Liga",
                "stickerType": "line",
                "dataType": "email",
                "imageType": "desc",
                "data": request.data['email'],
                "email": request.data['email'],
                "page":9,
                "rect": {
                    "lx": 355,
                    "ly": 102,
                    "tx": 555,
                    "ty": 202
                }
            },
                {
                "authority": "Vinculada a Correo Electronico por Liga",
                "stickerType": "line",
                "dataType": "email",
                "imageType": "desc",
                "data": 'contacto@taxinnova.mx',
                "email": 'contacto@taxinnova.mx',
                "page": 9,
                "rect": {
                    "lx": 55,
                    "ly": 102,
                    "tx": 255,
                    "ty": 202
                }
            }
            ],
            "workflow": {
                "expiration_date": ''+str(unaSemana.day)+'/'+str(unaSemana.month)+'/'+str(unaSemana.year)+'',
                "remind_every": '1d',
                "language": 'es',
                "attach_files": "true",
                "watchers": []
            }
        })

        json_respuesta = json.loads(response)
        print(json_respuesta)
        queryset = User.objects.get(id=request.data['id'])
        queryset.contract_sended = True
        queryset.save()

        queryset2 = UserProfile.objects.get(user_id=request.data['id'])
        queryset2.url_documento = json_respuesta['document_url']
        queryset2.ticket_documento = json_respuesta['document_ticket']
        queryset2.save()

        return Response(response, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='comprobar')
    def sendMessage(self, request, *args, **kwargs):
        codigo = request.data['codigo_comprobar']

    @action(detail=False, methods=['post'], url_path='update-password')
    def update_password(self, request, *args, **kwargs):
        """An endpoint for changing password."""

        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = {
            'message': 'Felicidades, ahora puedes iniciar sesión'
        }

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='recover-password-email')
    def recover_password_email(self, request, *args, **kwargs):
        """An endpoint to send an email to changing password."""
        serializer = PasswordRecoveryEmail(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['post'], url_path='recover-password')
    def recover_password(self, request, *args, **kwargs):
        """An endpoint for changing password."""
        serializer = PasswordRecovery(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='send-email-resetpass')
    def send_email_resetpass(self, request, *args, **kwargs):
        serializer = SendEmailChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'message': request.data
        }

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='token-4resetpass')
    def token_4resetpass(self, request, *args, **kwargs):
        """User account verification API view."""
        payload = jwt.decode(request.data['token'], settings.SECRET_KEY, algorithms=['HS256'])
        name = payload['name']
        username = payload['user']
        data = {
            'message': ' Hola {} ¿Estás listo para recuperar tu contraseña?'.format(name),
            'username': username
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def visitor_ip(self, request, *args, **kwargs):

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return Response(ip, status=status.HTTP_200_OK)
