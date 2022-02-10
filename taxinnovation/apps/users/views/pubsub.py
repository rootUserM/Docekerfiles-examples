"""User pub/sub views."""
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import http.client
import mimetypes
import random
import base64
import json
import http.client
import mimetypes
import requests


class UserPubSubViewSet(viewsets.GenericViewSet):
    """User PubSub API view."""

    @action(detail=False, methods=['post'])
    def alta_usuario_pub(self, request, *args, **kwargs):

        url = "http://35.227.68.19:8080/"
        payload="{\r\n    \"topic\": \"usuario\",\r\n    \"target\": \"cuenta\",\r\n    \"action\": \"alta\",\r\n    \"payload\": {\r\n        \"email\": \""+request.data['email']+"\",\r\n        \"username\": \""+request.data['username']+"\",\r\n        \"phoneNumber\": \""+request.data['phone_number'],+"\",\r\n        \"name\": \""+request.data['name']+"\",\r\n        \"lastName\": \""+request.data['last_name']+"\",\r\n        \"secondLastName\": \""+request.data['second_last_name']+"\"\r\n    }\r\n}"
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return Response(response.text, status=status.HTTP_200_OK)
