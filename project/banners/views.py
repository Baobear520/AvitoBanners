
from rest_framework import generics
from banners.models import Banner
from banners.serializers import BannerSerializer


class BannerList(generics.ListCreateAPIView):
    """Class for retrieving all banners or creating a banner"""

    queryset = Banner.objects.all()
    serializer_class  = BannerSerializer

class BannerDetail(generics.RetrieveUpdateDestroyAPIView):
    """Class for retireving/updating/deleting a banner"""
    
    queryset = Banner.objects.all()
    serializer_class  = BannerSerializer


