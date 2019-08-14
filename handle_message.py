# -*- encoding: utf-8 -*-
# from django.conf import settings
import requests
import json
import math
import random
from suite.chatbot.facebook.inspirations import actions, graph_api, nlp as textNLP


def handle_msg(webhook_event):
    responses = None
    try:
        if webhook_event.get('message'):
            message = webhook_event.get('message')
            # caso evento por botones
            if message.get('quick_reply'):
                handle_quick_replies(webhook_event)
            # caso evento por archivo adjunto
            elif message.get('attachments'):
                attachs = message.get('attachments')
                coords = attachs[0].get('payload').get('coordinates')
                if coords:
                    print('las coordenadas del usuario son: {}'.format(json.dumps(coords)))
            # caso evento por msg texto
            elif message.get('text'):
                print('Recibiendo mensaje de texto')
                handle_NLP(webhook_event)
        elif webhook_event.get('postback'):
            print('postback')
            handle_postback(webhook_event)
    except Exception as e:
        print(str(e))
        responses = {
            'text': 'An error has occured. We have been notified and will fix the issue shortly!'
        }


# Metodo para el manejo de Quick Replies
def handle_quick_replies(webhook_event):
    reply = webhook_event.get('message').get('quick_reply').get('payload')
    json_response = {
        'text': '¿Recomendarias nuestro servicio?',
        'replies': [
            {
                'content_type': 'text',
                'title': 'Si',
                'payload': 'siRecomienda',
            },
            {
                'content_type': 'text',
                'title': 'No',
                'payload': 'noRecomienda',
            }
        ]
    }
    if reply == 'rapidez' or reply == 'ubicacion' or reply == 'servicio':
        print('Reply  {}'.format(reply))
        actions.quick_replies(webhook_event, json_response)
    else:
        actions.send_text_message('Gracias por ayudarnos a mejorar', webhook_event)


# Metodo para la detección del envío de postbacks
def handle_postback(webhook_event):
    evento = webhook_event.get('postback').get('payload')
    if evento == 'encuestas':
        actions.quick_replies(webhook_event)
    elif evento == 'sucursales':
        handle_location(webhook_event)
    elif evento == 'inicio':
        graph_api.get_profile(webhook_event.get('sender').get('id'))
        actions.send_text_message("Hola soy el robot de Platzi y Developer Circle", webhook_event)
        actions.send_text_message("Te puedo ayudar con algunas dudas o encontrando sucursales cerca", webhook_event)
        

# Metodo para recibir ubicación
def handle_location(webhook_event):
    REPLIES_LOCATION = {
        'text': 'Por favor compartenos tu ubicacion para encontrar sucursales cercanas a ti',
        'replies': [
            {
                'content_type': 'location', # Deprecated
                'title': 'Enviar ubicacion',
                'payload': 'ubicacion',
            }
        ]
    }
    actions.quick_replies(webhook_event, REPLIES_LOCATION)


# Metodo para consumir servicios del procesador de lenguaje natural
def handle_NLP(webhook_event):
    nlp = webhook_event.get('message').get('nlp')
    text = ''
    saludos = textNLP.get('saludo')
    if len(nlp.get('entities')) and nlp.get('entities').get('saludo'):
        pos = random.randint(0, len(saludos))
        text = saludos[pos].get('text')
        actions.send_text_message(text, webhook_event)
    if nlp.get('entities').get('tiempoEntrega'):
        tiempo_entrega = textNLP.get('tiempoEntrega')
        text = tiempo_entrega[0].get('text')
        actions.send_text_message(text, webhook_event)
