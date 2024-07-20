
from django.urls import path

from banners import views


urlpatterns = [
    path('user-banner/',views.UserBannerView.as_view()),
    path('banner/',views.BannerList.as_view()),
    path('banner/<int:pk>',views.BannerDetail.as_view()),
    path('user/',views.UserList.as_view()),
    path('user/<int:pk>',views.UserDetail.as_view()),
]
