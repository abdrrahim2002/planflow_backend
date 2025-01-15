from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from .. import models


class Registration(APIView):
  
  def post(self, request):
    serializer = RegistrationSerializer(data=request.data)
    
    data = {}
    
    if serializer.is_valid():
      account = serializer.save()
      
      data['username'] = account.username
      data['email'] = account.email
      
      token = Token.objects.get(user=account).key
      data['token'] = token
      
      return Response(data, status=status.HTTP_201_CREATED)
    
    else :
      return Response( {'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


