from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DeviceToken
from .serializers import DeviceTokenSerializer
from share.utils import format_respone, LargeResultsSetPagination, get_paginated_response, create_paginated_response, format_date
from rest_framework import status, generics, filters

class DeviceTokenCreateView(generics.CreateAPIView):
    
    def post(self, request, *args, **kwargs):
        serializer = DeviceTokenSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response = format_respone(success=True, status=status.HTTP_201_CREATED, message="DeviceToken created successfully", data=serializer.data)
            return Response(response, status=response.get('status'))
        else:
            response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)
            return Response(response, status=response.get('status'))