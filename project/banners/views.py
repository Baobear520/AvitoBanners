
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from banners.models import Banner, UserBanner
from banners.serializers import BannerContentSerializer, BannerSerializer,UserSerializer


class BannerList(APIView):
    """
    List all banners, or create a new banner.
    """
    def get(self, request):
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        # banner = Banner.objects.create(**data)
        serializer = BannerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'banner_id': serializer.data['id']}, status=status.HTTP_201_CREATED)
        
    

class User(APIView):
    """
    Show current user's banner
    
    """
    def get(self, request):
        tag_id = request.query_params.get('tag_id')
        feature_id = request.query_params.get('feature_id')
        use_last_revision = request.query_params.get('use_last_revision', False)

        if not tag_id or not feature_id:
            return Response({"error": "Incorrect data. Please provide both tag_id and feature_id"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter banners based on tag_id and feature_id
        filtered_banners = Banner.objects.filter(tags=tag_id, feature=feature_id)
        banner = get_object_or_404(filtered_banners.only('content'))

        #Serializing only the content field
        serializer = BannerContentSerializer(banner)
        return Response(serializer.data)
        
