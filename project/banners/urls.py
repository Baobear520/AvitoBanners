
from django.urls import path
from banners import views


urlpatterns = [
    #path('user-banner/',),
    path('banner/',views.BannerList.as_view()),
    path('banner/<int:pk>',views.BannerDetail.as_view())
]
