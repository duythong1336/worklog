from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import status, generics
from .serializers import LoginSerializer, JWTTokenSerializer
from .models import JWTToken
from Employee.permissions import IsAdminOrStaff
from share.utils import format_respone
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user_data = serializer.validated_data
            response_data = format_respone(success=True, status=status.HTTP_200_OK, message="Login successfully", data=user_data)
            return Response(response_data, status=response_data.get('status'))
        else:
            response_data = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)
            return Response(response_data, status=response_data.get('status'))
        
class JWTTokenListView(APIView):
    # permission_classes = [IsAdminUser]
    permission_classes = [IsAdminOrStaff]
    
    def get(self, request, *args, **kwargs):
        Jwt = JWTToken.objects.all()  
        serializer = JWTTokenSerializer(Jwt, many=True)
        response = format_respone(success=True, status=status.HTTP_200_OK, message="Get JWT Token Success", data=serializer.data)
        
        return Response(response, status=response.get('status'))
    
class JWTTokenByUserListView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        jwt_tokens = JWTToken.objects.filter(user_id=user_id)
        serializer = JWTTokenSerializer(jwt_tokens, many=True)
        response = format_respone(success=True, status=status.HTTP_200_OK, message="Get JWT Tokens Success", data=serializer.data)
        
        return Response(response, status=response.get('status'))

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        try:
            user = request.user  # Lấy thông tin người dùng từ request
            access_token = request.auth  # Lấy access token từ request
            # print(access_token)

            if access_token and user.is_authenticated:
                # Tìm token trong cơ sở dữ liệu
                jwt_token = JWTToken.objects.filter(user_id = user.id, token=access_token).first()
                if jwt_token:
                    # Cập nhật trạng thái token
                    jwt_token.is_expired = True
                    jwt_token.save()
                    
                    response = format_respone(success=True, status=status.HTTP_200_OK, message="Logged out successfully", data=[])
                    return Response(response, status=response.get('status'))
                else:
                    response = format_respone(success=False, status=status.HTTP_404_NOT_FOUND, message="Token not found in database", data=[])
                    return Response(response, status=response.get('status'))
            else:
                response = format_respone(success=False, status=status.HTTP_401_UNAUTHORIZED, message="User is not authenticated", data=[])
                return Response(response, status=response.get('status'))
        except Exception as e:
            response = format_respone(success=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e), data=[])
            return Response(response, status=response.get('status'))
        
class LogoutAllView(APIView):
    def post(self, request):
        try:
            user = request.user  # Lấy người dùng hiện tại từ request
            if user.is_authenticated:

                jwt_tokens = JWTToken.objects.filter(user_id=user.id)
                
                if jwt_tokens:
                    jwt_tokens.update(is_expired=True)
                    # print(jwt_tokens)
                    response = format_respone(success=True, status=status.HTTP_200_OK, message="Logged out all sessions successfully", data=[])
                    return Response(response, status=response.get('status'))
                else:
                    response = format_respone(success=False, status=status.HTTP_404_NOT_FOUND, message="Token not found in database", data=[])
                    return Response(response, status=response.get('status'))
            else:
                response = format_respone(success=False, status=status.HTTP_401_UNAUTHORIZED, message="User is not authenticated", data=[])
                return Response(response, status=response.get('status'))
        except Exception as e:
            response = format_respone(success=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e), data=[])
            return Response(response, status=response.get('status'))
        
class LogoutDevicesView(APIView):
    def post(self, request):
        try:
            user = request.user  # Lấy người dùng hiện tại từ request
            if user.is_authenticated:
                device_ids = request.data.get('device_id', [])

                jwt_tokens = JWTToken.objects.filter(user_id=user.id, device_id__in=device_ids)
                # print(user.id)
                # print(device_ids)
                if jwt_tokens:
                # Cập nhật trạng thái is_expired của các mã thông báo này thành True
                    jwt_tokens.update(is_expired=True)
                # print(jwt_tokens)
                    response = format_respone(success=True, status=status.HTTP_200_OK, message="Logged out specified devices successfully", data=[])
                    return Response(response, status=response.get('status'))
                else:
                    response = format_respone(success=False, status=status.HTTP_404_NOT_FOUND, message="Token not found in database", data=[])
                    return Response(response, status=response.get('status'))
            else:
                response = format_respone(success=False, status=status.HTTP_401_UNAUTHORIZED, message="User is not authenticated", data=[])
                return Response(response, status=response.get('status'))
        except Exception as e:
            response = format_respone(success=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e), data=[])
            return Response(response, status=response.get('status'))