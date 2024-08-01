
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from banners import views


urlpatterns = [
    path('user-banner/',views.UserBannerView.as_view()),
    path('banner/',views.BannerList.as_view()),
    path('banner/<int:pk>',views.BannerDetail.as_view()),
    path('profile/',views.ProfileList.as_view()),
    path('profile/<int:pk>',views.ProfileDetail.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]
