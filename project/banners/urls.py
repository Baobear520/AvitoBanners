
from django.urls import path
from banners import views


urlpatterns = [
    path('user-banner/',views.User.as_view()),
    path('banner/',views.BannerList.as_view()),
    #path('banner/<int:pk>',views.Banner.as_view())
]
