from suite.chatbot.facebook.inspirations import graph_api

#quick replies
REPLIES_SURVEY = {
    'text': 'Por favor llena esta encuesta para que podamos mejorar',
    'replies': [
        {
            'content_type': 'text',
            'title': 'Servicio',
            'payload': 'servicio'
        },
        {
            'content_type': 'text',
            'title': 'Rapidez',
            'payload': 'rapidez'
        },
        {
            'content_type': 'text',
            'title': 'Ubicaciones',
            'payload': 'ubicacion'
        }
    ]
}

def get_profile_info(webhook_event):
    return graph_api.get_profile(int(webhook_event.get('sender').get('id')))


def send_text_message(text, webhook_event):
    profile = get_profile_info(webhook_event)
    json_request = {
        'recipient': {
            'id': int(webhook_event.get('sender').get('id'))
        },
        'message': {
            "text": '{}, {}'.format(profile.get('first_name'), text)
        }
    }
    return graph_api.call_send_api(json_request)


def quick_replies(webhook_event, replies=None):
    if replies is None:
        print('replies is NONE')
        replies = REPLIES_SURVEY
    json_request = {
        'recipient': {
            'id': int(webhook_event.get('sender').get('id'))
        },
        'message': {
            'text': replies.get('text'),
            'quick_replies': replies.get('replies')
        }
    }
    return graph_api.call_send_api(json_request)


def stores(webhook_event):
    json_request = {
        'recipient': {
            'id': int(webhook_event.get('sender').get('id'))
        },
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': 'Tienda del centro',
                            'image_url':'https://media4.s-nbcnews.com/i/newscms/2017_26/2053956/170627-better-grocery-store-main-se-539p_80a9ba9c8d466788799ca27568ee0d43.jpg',
                            'subtitle':'Direccion corta de la tienda',
                            'default_action': {
                                'type': 'web_url',
                                'url': 'https://goo.gl/maps/J5LQfLPy1s3zvtQZ6',
                                'messenger_extensions': 'FALSE',
                                'webview_height_ratio': 'COMPACT'
                            },
                            'buttons': [{
                                'type': 'web_url',
                                'url': 'https://goo.gl/maps/J5LQfLPy1s3zvtQZ6',
                                'title': 'Mostrar el mapa'
                            }, {
                                'type': 'phone_number',
                                'title': 'Llama a la tienda',
                                'payload': '+5215525250000'
                            }]
                        }
                    ]
                }
            }
        }
    }
    return graph_api.call_send_api(json_request)
