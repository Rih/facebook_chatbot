# -*- encoding: utf-8 -*-
from django.conf import settings
import requests
import json

URL = 'https://graph.facebook.com/v3.3'
GRAPH_HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}


def call_send_api(request_body):
    uri = '{}/me/messages?access_token={}'.format(URL, settings.FB_ACCESS_TOKEN)
    print uri
    print 'request_body'
    print request_body
    response = requests.post(url=uri, headers=GRAPH_HEADERS, json=request_body)
    json_response = json.loads(response.text)
    return json_response


def get_profile(sender_id):
    fields = 'first_name, last_name, locale, timezone'
    uri = '{}/{}?access_token={}&fields={}'.format(URL, sender_id, settings.FB_ACCESS_TOKEN, fields)
    response = requests.get(url=uri, headers=GRAPH_HEADERS)
    json_response = json.loads(response.text)
    return json_response

