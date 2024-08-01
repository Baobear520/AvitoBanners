from django.forms import ValidationError
from django.db import transaction
from django.http import Http404

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authtoken.models import Token

from banners.models import Banner, BannerTagFeature, UserBanner
from banners.serializers import BannerSerializer, BannerTagFeatureSerializer, UpdateBannerSerializer, UserSerializer


class BannerList(APIView):
    """
    List all banners with filtering by tag_id and/or feature_id, 
    or create a new banner.
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        tag_id = request.query_params.get('tag_id')
        feature_id = request.query_params.get('feature_id')

        # Initial queryset
        queryset = Banner.objects.all()

        # Apply filtering based on query parameters
        if tag_id and feature_id:
            queryset = queryset.filter(tags__id=tag_id, feature__id=feature_id)
        elif tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        elif feature_id:
            queryset = queryset.filter(feature__id=feature_id)
        
        # Prefetch related tags and features
        queryset = queryset.prefetch_related('tags', 'feature')
        
        if not queryset.exists():
            return Response(
                {"error": "No banner found matching the given parameters"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Apply pagination
        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request)

        # Serialize data
        serializer = BannerSerializer(page, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
        
        
    def post(self, request):
        data = request.data
        serializer = BannerSerializer(data=data)

        try:
            with transaction.atomic():
                serializer.is_valid(raise_exception=True)
                banner = serializer.save()

                # Process tags and create BannerTagFeature instances
                tags = request.data.get('tags')
                if not tags:
                    banner.delete()
                    return Response(
                        {"error": "You must provide tag_ids to create a banner"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                for tag_id in tags:
                    tag_feature_data = {
                        'tag': tag_id,
                        'banner': banner.id,
                        'feature': request.data.get('feature')
                    }

                    banner_tag_feature_serializer = BannerTagFeatureSerializer(data=tag_feature_data)
                    banner_tag_feature_serializer.is_valid(raise_exception=True)
                    banner_tag_feature_serializer.save()

                # Render only the required fields from the banner object
                return Response(
                    data={'banner_id': serializer.data['id']}, 
                    status=status.HTTP_201_CREATED
                    )

        except ValidationError as e:
            if banner.id:
                banner.delete()
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


class BannerDetail(APIView):
    """Update/delete a banner"""

    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Banner.objects.get(pk=pk)
        except Banner.DoesNotExist:
            raise Http404
        
    def get(self,request,pk):
        banner = self.get_object(pk)
        serializer = BannerSerializer(banner)
        return Response(serializer.data,status=status.HTTP_200_OK)

        
    def patch(self, request, pk):
        banner = self.get_object(pk)
        data = request.data

        try:
            with transaction.atomic():
                # Update the Banner object
                serializer = UpdateBannerSerializer(banner, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                banner = serializer.save()

                # Process tags and update/create BannerTagFeature instances
                tags = data.get('tags')
                if tags is not None:
                    BannerTagFeature.objects.filter(banner=banner).delete()  # Delete old tag-feature relations

                    for tag_id in tags:
                        tag_feature_data = {
                            'tag': tag_id,
                            'banner': banner.id,
                            'feature': data.get('feature', banner.feature.id)
                        }
                        banner_tag_feature_serializer = BannerTagFeatureSerializer(data=tag_feature_data)
                        banner_tag_feature_serializer.is_valid(raise_exception=True)
                        banner_tag_feature_serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        banner = self.get_object(pk)
        banner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UserBannerView(APIView):
    """
    Show current user's banner
    
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        tag_id = request.query_params.get('tag_id')
        feature_id = request.query_params.get('feature_id')
        use_last_revision = request.query_params.get('use_last_revision', 'False').lower()==True

        if not tag_id or not feature_id:
            return Response(
                {"error": "Incorrect data. Please provide correct tag_id and feature_id"}, 
                status=status.HTTP_400_BAD_REQUEST)
        
        # if use_last_revision:
        #     do smth
        # else: 
        # do smth else
        
        try:
            queryset = Banner.objects.get(tags__id=tag_id, feature__id=feature_id)
            serializer = BannerSerializer(queryset)
            return Response(serializer.data['content'],status=status.HTTP_200_OK)
        
        except Banner.DoesNotExist:
            return Response(
                {"error": "No banner matching the given parameters found"},
                status=status.HTTP_404_NOT_FOUND)
        
        
class UserList(APIView):
    
    """
    Show the list of all users
    
    """
    
    def get(self,request):
        try:
            queryset = UserBanner.objects.all()
            users = UserSerializer(queryset,many=True)
            return Response(data=users.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_404_NOT_FOUND)
    
  
    def post(self,request):
        data = request.data
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class UserDetail(APIView):
    """
    Show details of the user
    
    """
    
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return UserBanner.objects.get(pk=pk)
        except UserBanner.DoesNotExist:
            raise Http404
        
    def get(self,request,pk):

        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)



class LoginUser(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        #password = request.data.get('password')

        if not username:
            return Response({'error': 'Please provide username.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserBanner.objects.get(username=username)
        except UserBanner.DoesNotExist:
            return Response({'error': f"User {username} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({'token': token.key}, status=status.HTTP_200_OK)
