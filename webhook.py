import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from suite.chatbot.facebook.inspirations import handle_message as handle

@csrf_exempt
def notification(request):
    """This is the webhook called from PayU
    """
    if request.method == 'POST':
        body = json.loads(request.body)
        print body
        if body.get('object') == 'page':
            for entry in body.get('entry'):
                msg = entry.get('messaging')
                webhook_event = msg[0]
                handle.handle_msg(webhook_event)
            return HttpResponse("EVENT_RECEIVED", status=200)
        else:
            return HttpResponse("", status=404)
    if request.method == 'GET':
        try:
            print request.GET
            mode = request.GET.get('hub.mode')
            challenge = request.GET.get('hub.challenge')
            token = request.GET.get('hub.verify_token')
            print mode
            print challenge
            print token
            if mode == "subscribe" and token == settings.FB_VERIFY_TOKEN:
                print('webhook ok')
                return HttpResponse(challenge, status=200)
            
                
        except Exception as e:
            return HttpResponse(
                json.dumps({'status': 'transaction_id not defined'}),
                content_type='application/json'
            )
    return HttpResponse(
                json.dumps({'status': 'method POST not allowed'}),
                content_type='application/json'
            )
