
from erp import models, schema
from django.http import HttpResponse

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path not in ['/login/','/delete-token/']:
            token = request.META.get('HTTP_AUTHORIZATION')
            if token is None:
                return HttpResponse('You must provide a new Token', status=401)
            else:
                if not models.Token.objects.filter(token=token).exists():
                    return HttpResponse('Invalid token', status=401)
                x = schema.updateToken(token)
                if x.status_code == 401:
                    return HttpResponse('Expired token', status=401)
                request.META['REMOTE_USER'] = schema.getUserByToken(token).username
        return response
        
    
        