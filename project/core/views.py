
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from core.models import AvitoUser
from core.serializers import CreateAvitoUserSerializer, ViewAvitoUserSerializer

class AvitoUserList(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return super().get_permissions()
    
    def get(self, request):
        users = AvitoUser.objects.all()
        serializer = ViewAvitoUserSerializer(users,many=True)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def post(self,request):
        data = request.data
        serializer = CreateAvitoUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data,status=status.HTTP_201_CREATED) 
    

