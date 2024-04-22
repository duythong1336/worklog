from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from JWTToken.models import JWTToken 

class CheckTokenExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                user, token = self.jwt_auth.authenticate(request)
                if isinstance(token, AccessToken):

                    jwt_token = JWTToken.objects.filter(token=token).first()
                    if jwt_token and jwt_token.is_expired:
                        return JsonResponse({'detail': 'Token has expired.'}, status=401)
                else:
                    return JsonResponse({'detail': 'Invalid token.'}, status=401)
            except Exception as e:
                return JsonResponse({'detail': str(e)}, status=401)
        
        response = self.get_response(request)
        return response
